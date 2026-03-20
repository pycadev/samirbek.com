importScripts("https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js");

let pyodide;

async function init() {
    pyodide = await loadPyodide({
        indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.0/full/"
    });
    
    // Setup I/O
    pyodide.runPython(`
        import sys, io, builtins
        from js import XMLHttpRequest

        class WorkerStdout(io.TextIOBase):
            def write(self, s):
                self.__class__.send_output(s)
                return len(s)
            
            @staticmethod
            def send_output(s):
                from js import postMessage
                import json
                postMessage(json.dumps({"type": "stdout", "data": s}))

        class WorkerInput:
            def readline(self, size=-1):
                from js import XMLHttpRequest
                xhr = XMLHttpRequest.new()
                # BLOCKING Sync XHR to Django
                xhr.open("GET", "/api/lab/input/request/?session_id=user1", False)
                xhr.send()
                
                if xhr.status == 200:
                    import json
                    res = json.loads(xhr.responseText)
                    return res["data"] + "\\n"
                return ""

        sys.stdout = WorkerStdout()
        sys.stderr = WorkerStdout()
        sys.stdin = WorkerInput()

        def worker_input(p=""):
            if p: WorkerStdout.send_output(str(p))
            return sys.stdin.readline().strip("\\n")

        builtins.input = worker_input
    `);
    
    postMessage(JSON.stringify({type: "status", data: "ready"}));
}

onmessage = async (e) => {
    const data = JSON.parse(e.data);
    if (data.type === "init") {
        await init();
    } else if (data.type === "run" || data.type === "repl") {
        try {
            const result = await pyodide.runPythonAsync(data.code);
            
            // For REPL: auto-print expression results (if not None)
            if (data.type === "repl" && result !== undefined && result !== null) {
                // Check if result is not None in Python sense
                const isNone = pyodide.runPython(`type(${JSON.stringify(result)}) is type(None) if isinstance(${JSON.stringify(result)}, str) else False`); 
                // Simplified check: just print if it's not undefined
                pyodide.runPython(`print(repr(${JSON.stringify(result)}))`);
            }
            
            postMessage(JSON.stringify({type: "status", data: "finished"}));
        } catch (err) {
            postMessage(JSON.stringify({type: "error", data: err.message}));
        }
    }
};
