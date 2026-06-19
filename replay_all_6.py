import json
import os

log_file = '/Users/charlie/.gemini/antigravity-ide/brain/33a79cb7-9abc-443d-b35e-6e7b460dfcbd/.system_generated/logs/transcript.jsonl'

with open(log_file, 'r') as f:
    for line in f:
        try:
            data = json.loads(line)
            if 'tool_calls' in data:
                for call in data['tool_calls']:
                    name = call['name']
                    if 'replace' in name:
                        args = call.get('args', {})
                        target = args.get('TargetFile', '').strip('"').strip("'")
                        
                        if not target.endswith('.html'):
                            continue
                        
                        if 'multi' not in name:
                            print(f"Replace in: {target}")
                            try:
                                with open(target, 'r') as file:
                                    content = file.read()
                                target_content = args.get('TargetContent', '')
                                if isinstance(target_content, str):
                                    target_content = target_content.strip('"').strip("'")
                                else:
                                    target_content = str(target_content).strip('"').strip("'")
                                    
                                # wait! The JSON args might be strings that represent JSON!
                                # "args": { "TargetFile": "\"/Users/...\"", "TargetContent": "\"<div>...\"" }
                                # NO! Let me just use json.loads(args) if args is a string.
                                # But args is a dictionary here.
                                
                                # Let's just strip surrounding quotes
                                target_content = args.get('TargetContent', '')
                                if target_content.startswith('"') and target_content.endswith('"'):
                                    target_content = target_content[1:-1].replace('\\"', '"').replace('\\n', '\n')
                                
                                replacement = args.get('ReplacementContent', '')
                                if replacement.startswith('"') and replacement.endswith('"'):
                                    replacement = replacement[1:-1].replace('\\"', '"').replace('\\n', '\n')
                                    
                                if target_content in content:
                                    content = content.replace(target_content, replacement)
                                    with open(target, 'w') as file:
                                        file.write(content)
                                else:
                                    print(f"  -> Target not found in {target}!")
                            except Exception as e:
                                print(f"Error: {e}")
                        else:
                            print(f"Multi-replace in: {target}")
                            try:
                                with open(target, 'r') as file:
                                    content = file.read()
                                chunks_str = args.get('ReplacementChunks', '')
                                if isinstance(chunks_str, str):
                                    try:
                                        chunks = json.loads(chunks_str.strip('"').replace('\\"', '"'))
                                    except:
                                        chunks = []
                                else:
                                    chunks = chunks_str
                                    
                                for chunk in chunks:
                                    target_content = chunk.get('TargetContent', '')
                                    replacement = chunk.get('ReplacementContent', '')
                                    if target_content in content:
                                        content = content.replace(target_content, replacement)
                                    else:
                                        print(f"  -> Target chunk not found in {target}!")
                                with open(target, 'w') as file:
                                    file.write(content)
                            except Exception as e:
                                print(f"Error: {e}")
        except Exception as e:
            pass

print("Replay finished.")
