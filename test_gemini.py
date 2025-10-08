"""
Test Gemini API integration
"""
import google.generativeai as genai

# Configure API
api_key = "AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M"
genai.configure(api_key=api_key)

print("Testing Gemini API...")
print("-" * 50)

# Try gemini-1.5-flash
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Say 'Hello! I'm working!' in a friendly way.")
    print("✅ SUCCESS with gemini-1.5-flash!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR with gemini-1.5-flash: {e}")

print("\n" + "-" * 50)

# Try gemini-pro
try:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say 'Hello! I'm working!' in a friendly way.")
    print("✅ SUCCESS with gemini-pro!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR with gemini-pro: {e}")

print("\n" + "-" * 50)

# List available models
print("\nListing available models:")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"  - {model.name}")
except Exception as e:
    print(f"Error listing models: {e}")
