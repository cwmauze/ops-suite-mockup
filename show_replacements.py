import json

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    if 'replace' in call['name']:
                        args = call.get('args', {})
                        if 'flightlog.html' in args.get('TargetFile', ''):
                            print(f"\n--- REPLACEMENT on {args['TargetFile']} ---")
                            if 'Instruction' in args: print(f"Instruction: {args['Instruction']}")
                            if 'TargetContent' in args:
                                print(f"Target Length: {len(args['TargetContent'])}")
                            if 'ReplacementChunks' in args:
                                print(f"Chunks: {len(args['ReplacementChunks'])}")
        except Exception as e:
            pass
