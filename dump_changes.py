import json

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    name = call['name']
                    if 'replace' in name or 'write' in name or 'command' in name:
                        print(f"Tool: {name}")
                        args = call.get('args', {})
                        if 'TargetFile' in args:
                            print(f"Target: {args['TargetFile']}")
                        if 'CommandLine' in args:
                            cmd = args['CommandLine']
                            if 'python' in cmd or 'cp ' in cmd or 'mv ' in cmd or 'sed ' in cmd:
                                print(f"Command: {cmd[:100]}...")
        except Exception as e:
            pass
