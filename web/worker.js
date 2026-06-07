const PYODIDE_URL = 'https://cdn.jsdelivr.net/pyodide/v0.26.4/full/';

importScripts(PYODIDE_URL + 'pyodide.js');

let pyodide = null;
let running = false;
const __keysPressed = new Set();

const KEY_MAP = {
    ' ': 'space',
    'ArrowUp': 'Up',
    'ArrowDown': 'Down',
    'ArrowLeft': 'Left',
    'ArrowRight': 'Right',
};

async function init(moduleSources) {
    try {
        self.postMessage({ type: 'status', text: 'Loading Python runtime...' });

        pyodide = await loadPyodide({ indexURL: PYODIDE_URL });

        self.postMessage({ type: 'status', text: 'Installing shim modules...' });

        installFiles(moduleSources);
        setupStopHandler();
        cachePythonFunctions();

        self.postMessage({ type: 'ready' });
    } catch (err) {
        self.postMessage({ type: 'error', message: 'Init failed: ' + err.message, traceback: err.stack });
    }
}

function installFiles(sources) {
    for (const [path, content] of Object.entries(sources)) {
        const parts = path.split('/').filter(p => p.length > 0);
        let dir = '';
        for (let i = 0; i < parts.length - 1; i++) {
            dir += '/' + parts[i];
            try { pyodide.FS.mkdir(dir); } catch (_) {}
        }
        pyodide.FS.writeFile(path, content);
    }

    pyodide.runPython(`
import sys
sys.path.insert(0, '/modules')
`);
}

function setupStopHandler() {
    let useAsyncSleep = false;

    if (typeof SharedArrayBuffer !== 'undefined') {
        const sleepBuffer = new SharedArrayBuffer(4);
        const sleepInterrupt = new Int32Array(sleepBuffer);
        Atomics.store(sleepInterrupt, 0, 0);
        self.__sleepInterrupt = sleepInterrupt;
        self.__sleep_js = function (ms) {
            Atomics.wait(self.__sleepInterrupt, 0, 0, ms);
        };
        useAsyncSleep = true;
    }

    if (useAsyncSleep) {
        pyodide.runPython(`
import time as _time
import js

_stop_requested = False

def _browser_sleep(seconds):
    ms = int(seconds * 1000)
    if ms > 0:
        js.__sleep_js(ms)
    if _stop_requested:
        raise KeyboardInterrupt("Execution stopped")

_time.sleep = _browser_sleep
`);
    } else {
        pyodide.runPython(`
import time as _time
_stop_requested = False
_original_sleep = _time.sleep

def _browser_sleep(seconds):
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.sleep(seconds))
    except:
        _original_sleep(seconds)
    if _stop_requested:
        raise KeyboardInterrupt("Execution stopped")

_time.sleep = _browser_sleep
`);
    }
}

function cachePythonFunctions() {
    pyodide.runPython(`
import turtle as _turtle_mod
_keydown_cb = _turtle_mod._handle_keydown
_keyup_cb = _turtle_mod._handle_keyup
_click_cb = _turtle_mod._handle_click
_resize_cb = _turtle_mod._resize
_init_cb = _turtle_mod._init
`);
}

function initCanvas(width, height) {
    if (!pyodide) return;
    try {
        const fn = pyodide.globals.get('_init_cb');
        if (!fn) {
            self.postMessage({ type: 'error', message: 'Canvas init: _init_cb not found' });
            return;
        }
        fn(width, height);
    } catch (err) {
        self.postMessage({ type: 'error', message: 'Canvas init: ' + err.message });
    }
}

async function runCode(code) {
    if (running) return;
    running = true;

    pyodide.runPython(`_stop_requested = False`);
    if (self.__sleepInterrupt) {
        Atomics.store(self.__sleepInterrupt, 0, 0);
    }

    self.postMessage({ type: 'running' });

    // Split user code at `while True:`
    const loopMatch = code.match(/([\s\S]*?)while\s+True\s*:\s*\n((?:[ \t]+\S[\s\S]*?))(?=\n\S|\n*$)/);
    
    if (loopMatch) {
        let setupCode = loopMatch[1].trimEnd();
        let loopBody = loopMatch[2];
        
        // Determine indentation of loop body
        const indentMatch = loopBody.match(/^(\s+)/);
        const indent = indentMatch ? indentMatch[1].length : 0;
        
        // Dedent and clean loop body
        const dedented = loopBody.split('\n').map(l => l.substring(indent)).join('\n');
        
        // Remove sleep() lines from the loop body
        const cleanedBody = dedented.split('\n').filter(l => !l.trim().match(/^sleep\s*\(/)).join('\n');

        const escapedBody = cleanedBody.replace(/\\/g, '\\\\').replace(/`/g, '\\`').replace(/\${/g, '\\${');
        const wrappedCode = `
import js as _js

def _patched_isPressed(self, k):
    return _js.__isKeyPressed(k)

import tphysics as _tp
_tp.KeyListener.isPressed = _patched_isPressed
_stop_requested = False

${setupCode}

def __game_step():
    exec("""${escapedBody}""", globals())
`;
        try {
            await pyodide.runPythonAsync(wrappedCode);
            self.__gameStep = pyodide.globals.get('__game_step');
            if (self.__gameStep) {
                self.postMessage({ type: 'tick_start' });
                return;
            }
        } catch (err) {
            self.postMessage({ type: 'error', message: err.message, traceback: err.stack || '' });
        }
        running = false;
        self.__gameStep = null;
        self.postMessage({ type: 'done' });
        return;
    }
    
    // Fallback: run code as-is
    try {
        await pyodide.runPythonAsync(code);
    } catch (err) {
        if (err.message !== 'Execution stopped') {
            self.postMessage({ type: 'error', message: err.message, traceback: err.stack || '' });
        }
    } finally {
        running = false;
        self.postMessage({ type: 'done' });
    }
}

function stopCode() {
    try {
        self.__gameStep = null;
        if (self.__sleepInterrupt) {
            Atomics.store(self.__sleepInterrupt, 0, 1);
            Atomics.notify(self.__sleepInterrupt, 0);
        }
        pyodide.runPython(`_stop_requested = True`);
        if (running) {
            running = false;
            self.postMessage({ type: 'done' });
        }
    } catch (_) {}
}

function handleKeyDown(key) {
    const mapped = KEY_MAP[key] || key.toLowerCase();
    __keysPressed.add(mapped);
    if (!pyodide) return;
    try {
        const fn = pyodide.globals.get('_keydown_cb');
        if (fn) fn(mapped);
    } catch (_) {}
}

function handleKeyUp(key) {
    const mapped = KEY_MAP[key] || key.toLowerCase();
    __keysPressed.delete(mapped);
    if (!pyodide) return;
    try {
        const fn = pyodide.globals.get('_keyup_cb');
        if (fn) fn(mapped);
    } catch (_) {}
}

self.__isKeyPressed = function (key) {
    return __keysPressed.has(key);
};

function handleClick(x, y, button) {
    if (!pyodide) return;
    try {
        const fn = pyodide.globals.get('_click_cb');
        if (fn) fn(x, y, button);
    } catch (_) {}
}

function handleResize(width, height) {
    if (!pyodide) return;
    try {
        const fn = pyodide.globals.get('_resize_cb');
        if (fn) fn(width, height);
    } catch (_) {}
}

self.sendFrame = function (imageData) {
    self.postMessage({ type: 'frame', imageData: imageData }, [imageData.data.buffer]);
};

self.onmessage = async function (e) {
    const { type } = e.data;

    switch (type) {
        case 'init':
            await init(e.data.moduleSources);
            break;
        case 'run':
            await runCode(e.data.code);
            break;
        case 'stop':
            stopCode();
            break;
        case 'keydown':
            handleKeyDown(e.data.key);
            break;
        case 'keyup':
            handleKeyUp(e.data.key);
            break;
        case 'click':
            handleClick(e.data.x, e.data.y, e.data.button);
            break;
        case 'init_canvas':
            initCanvas(e.data.width, e.data.height);
            break;
        case 'resize':
            handleResize(e.data.width, e.data.height);
            break;
        case 'tick':
            if (self.__gameStep) {
                try {
                    self.__gameStep();
                } catch (err) {
                    self.postMessage({ type: 'error', message: err.message, traceback: err.stack || '' });
                    running = false;
                    self.__gameStep = null;
                    self.postMessage({ type: 'done' });
                }
            }
            break;
    }
};
