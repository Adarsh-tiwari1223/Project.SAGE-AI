from google import genai

class Gemenai:
    def Genai(self, command):
        try:
            client = genai.Client(api_key="AIzaSyAqtIjCK4yYOIfqXTEXucF-Np_N88DiKw8")
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=command
            )
            if response and response.text:
                return response.text
            else:
                return "No response from the server."
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
