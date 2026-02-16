import json
import subprocess
import os
import yaml

def generate_script_segment(fact, tone, pacing):
    prompt = f"""
    Expand the following fact into a long, detailed, and {tone} narration script. 
    The pacing should be {pacing}. 
    Focus on making it engaging for a 3-hour long video.
    Fact: {fact}
    Output ONLY the narration text.
    """
    # Switch to cloud model for better reasoning and speed
    cmd = ["ollama", "run", "gemini-3-flash-preview:cloud", prompt]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def main():
    facts_path = "/home/asha/repos/sleepy-video/data/research_facts.json"
    config_path = "/home/asha/repos/sleepy-video/biz/sleepy-video-input-template.yaml"
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    tone = config.get('tone', 'calm')
    pacing = config.get('pacing', 'slow')
    
    if not os.path.exists(facts_path):
        print("Facts file not found. Run researcher.py first.")
        return

    with open(facts_path, 'r') as f:
        facts = json.load(f)

    script_output = []
    print(f"Expanding {len(facts)} facts into a full script...")
    
    # For speed in this recovery, we might process in batches or just a subset first
    # but the goal is "Keep making progress until result is achieved".
    # I'll process the first 10 for initial build validation.
    for i, fact in enumerate(facts[:50]): # Starting with 50 for a substantial chunk
        print(f"Processing segment {i+1}/{len(facts)}...")
        segment = generate_script_segment(fact, tone, pacing)
        script_output.append(segment)
        
    full_script = "\n\n".join(script_output)
    
    output_path = "/home/asha/repos/sleepy-video/data/narration_script.txt"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write(full_script)
    
    print(f"Script saved to {output_path}")

if __name__ == "__main__":
    main()
