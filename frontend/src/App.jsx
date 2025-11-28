import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';
import { Play, Wrench, RotateCcw, Terminal, Code, Activity } from 'lucide-react';

const API_URL = 'http://localhost:8000';

const TEST_CASE_1 = `class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def preorder(root, res):
    if not root:
        return
    
    preorder(root.left, res)
    res.append(root.val)
    preorder(root.right, res)

root = Node(1)
root.left = Node(2)
root.right = Node(3)

res = []
preorder(root, res)
print(res)`;

const TEST_CASE_2 = `def fib(n, memo={}):
    if n <= 1:
        return n

    if n in memo:
        return memo[0]   # BUG: wrong key returned

    memo[n] = fib(n-1, memo) + fib(n-2, memo)
    return memo[n]

print(fib(10))`;

function App() {
    const [code, setCode] = useState(TEST_CASE_1);
    const [logs, setLogs] = useState([]);
    const [isRunning, setIsRunning] = useState(false);

    const addLog = (type, content, details = null) => {
        setLogs(prev => [...prev, { type, content, details, timestamp: new Date().toLocaleTimeString() }]);
    };

    const handleRun = async () => {
        setIsRunning(true);
        addLog('info', 'Running code...');
        try {
            const res = await axios.post(`${API_URL}/run`, { code });
            if (res.data.success) {
                addLog('success', `Output:\n${res.data.output}`);
            } else {
                addLog('error', `Error:\n${res.data.error}`);
            }
        } catch (err) {
            addLog('error', 'Failed to connect to backend.');
        }
        setIsRunning(false);
    };

    const handleRepair = async () => {
        setIsRunning(true);
        addLog('info', 'Starting Autonomous Repair Loop...');
        try {
            const res = await axios.post(`${API_URL}/repair`, { code });
            const history = res.data.history;

            history.forEach((step, index) => {
                setTimeout(() => {
                    addLog('info', `Iteration ${step.iteration}: ${step.status}`);

                    if (step.execution) {
                        if (step.execution.success) {
                            addLog('success', `Execution Output: ${step.execution.output}`);
                        } else {
                            addLog('error', `Execution Error: ${step.execution.error}`);
                        }
                    }

                    if (step.patch && step.patch.patch_applied) {
                        addLog('success', `Patch Applied: ${step.patch.explanation}`, step.patch.diff);
                        setCode(step.patch.new_code);
                    } else if (step.status === 'no_patch_found') {
                        addLog('error', 'No patch found for this issue.');
                    }
                }, index * 1000); // Stagger logs for effect
            });

        } catch (err) {
            addLog('error', 'Repair failed.');
        }
        setIsRunning(false);
    };

    return (
        <div className="container">
            <header className="header">
                <h1><Activity className="text-blue-500" /> Autonomous Debugger</h1>
                <div className="controls">
                    <button className="btn btn-secondary" onClick={() => setCode(TEST_CASE_1)}>Test Case 1</button>
                    <button className="btn btn-secondary" onClick={() => setCode(TEST_CASE_2)}>Test Case 2</button>
                </div>
            </header>

            <div className="main-layout">
                <div className="panel">
                    <div className="panel-header">
                        <span className="panel-title"><Code size={16} style={{ display: 'inline', marginRight: '5px' }} /> Code Editor</span>
                        <div className="controls">
                            <button className="btn btn-primary" onClick={handleRun} disabled={isRunning}>
                                <Play size={16} /> Run
                            </button>
                            <button className="btn btn-primary" style={{ backgroundColor: 'var(--success-color)' }} onClick={handleRepair} disabled={isRunning}>
                                <Wrench size={16} /> Auto-Repair
                            </button>
                        </div>
                    </div>
                    <div className="editor-container">
                        <Editor
                            height="100%"
                            defaultLanguage="python"
                            theme="vs-dark"
                            value={code}
                            onChange={(value) => setCode(value)}
                            options={{
                                minimap: { enabled: false },
                                fontSize: 14,
                                scrollBeyondLastLine: false,
                            }}
                        />
                    </div>
                </div>

                <div className="panel">
                    <div className="panel-header">
                        <span className="panel-title"><Terminal size={16} style={{ display: 'inline', marginRight: '5px' }} /> Execution Log</span>
                        <button className="btn btn-secondary" onClick={() => setLogs([])}><RotateCcw size={14} /></button>
                    </div>
                    <div className="output-container">
                        {logs.length === 0 && <div style={{ color: 'var(--text-secondary)', textAlign: 'center', marginTop: '2rem' }}>Ready to debug...</div>}
                        {logs.map((log, i) => (
                            <div key={i} className={`log-entry ${log.type}`}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                                    <strong>[{log.timestamp}]</strong>
                                </div>
                                <div>{log.content}</div>
                                {log.details && (
                                    <div className="diff-view">
                                        {log.details.split('\n').map((line, j) => {
                                            let className = 'diff-line';
                                            if (line.startsWith('+')) className += ' diff-add';
                                            if (line.startsWith('-')) className += ' diff-remove';
                                            return <span key={j} className={className}>{line}</span>;
                                        })}
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
