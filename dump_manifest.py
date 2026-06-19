import json
import os

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

# We'll extract all 'replace_file_content' and 'multi_replace_file_content' actions.
# We also need the file content from the git commit to start with.
# Actually, wait, let's just dump the exact ReplacementContent chunks for manifest.html so I can see if it's feasible to just paste them in manually or if there are too many.

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    name = call['name']
                    if 'replace' in name:
                        args = call.get('args', {})
                        target_file = args.get('TargetFile', '')
                        if 'manifest.html' in target_file:
                            print(f"\n====================== {name} on manifest.html ======================")
                            if 'Instruction' in args: print(f"Instruction: {args['Instruction']}")
                            if 'ReplacementContent' in args:
                                print(args['ReplacementContent'])
                            elif 'ReplacementChunks' in args:
                                for chunk in args['ReplacementChunks']:
                                    print("--- CHUNK ---")
                                    print(chunk.get('ReplacementContent', ''))
        except Exception as e:
            pass
