# test_gemini.py
import google.generativeai as genai
import os

def test_gemini_api():
    """Test if Gemini API key is working"""
    
    # Your API key - try both direct and environment variable
    API_KEY = "AIzaSyCkgpVqjDj2PV7L6rVRwyGq7Cf2QjKYUGo"
    env_key = os.getenv('GOOGLE_API_KEY')
    
    print("🧪 TESTING GEMINI API KEY")
    print("=" * 50)
    
    # Test direct key
    print(f"🔑 Direct API Key: {API_KEY[:10]}...{API_KEY[-4:]}")
    print(f"🔑 Key length: {len(API_KEY)}")
    print(f"🔑 Env API Key: {'SET' if env_key else 'NOT SET'}")
    
    # Test 1: Basic configuration
    try:
        genai.configure(api_key=API_KEY)
        print("✅ Configuration successful")
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False
    
    # Test 2: Model creation
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Model creation successful")
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False
    
    # Test 3: Simple API call
    try:
        print("🔄 Testing API call...")
        response = model.generate_content(
            "Say 'API TEST SUCCESSFUL' in your response.",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=20,
                temperature=0.1
            )
        )
        print("✅ API call successful")
        print(f"📝 Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"❌ API call failed: {e}")
        
        # Provide specific error solutions
        error_str = str(e).lower()
        if "api key" in error_str:
            print("\n💡 SOLUTION: Your API key is invalid or expired")
            print("   - Get a new key from: https://aistudio.google.com/app/apikey")
        elif "quota" in error_str:
            print("\n💡 SOLUTION: API quota exceeded")
            print("   - Check billing in Google Cloud Console")
        elif "permission" in error_str:
            print("\n💡 SOLUTION: Gemini API not enabled")
            print("   - Enable Gemini API in Google Cloud Console")
        elif "location" in error_str or "region" in error_str:
            print("\n💡 SOLUTION: Regional restriction")
            print("   - Try with VPN or check API availability")
        elif "unavailable" in error_str:
            print("\n💡 SOLUTION: Service temporarily unavailable")
            print("   - Try again in a few minutes")
        else:
            print(f"\n💡 Unknown error - check Google Cloud Console")
        
        return False

def test_alternative_models():
    """Test with alternative models if main one fails"""
    API_KEY = "AIzaSyCkgpVqjDj2PV7L6rVRwyGq7Cf2QjKYUGo"
    
    print("\n🔄 Testing alternative models...")
    models_to_try = ['gemini-1.5-flash', 'gemini-1.0-pro', 'models/gemini-1.5-flash']
    
    for model_name in models_to_try:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'OK'")
            print(f"✅ {model_name}: WORKING - {response.text[:30]}")
            return True
        except Exception as e:
            print(f"❌ {model_name}: FAILED - {str(e)[:50]}")
    
    return False

if __name__ == "__main__":
    print("🚀 Starting Gemini API Diagnostics...\n")
    
    # Test main functionality
    success = test_gemini_api()
    
    if not success:
        print("\n🔄 Trying alternative models...")
        test_alternative_models()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ALL TESTS PASSED - Your API key is working!")
    else:
        print("❌ API KEY ISSUE DETECTED - Check solutions above")
    
    print("\n📋 Next steps:")
    print("1. If API works: Check your question generation code")
    print("2. If API fails: Get new key from https://aistudio.google.com/app/apikey")