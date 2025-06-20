# from flask import Flask, request, render_template
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os

# app = Flask(__name__, template_folder='C:\xampp\htdocs\tour_recommendation_system')

# load_dotenv()
# api_key = os.getenv("GEMINI_API_KEY")


# if not api_key:
#     print("not found API")

# genai.configure(api_key=api_key)
# generation_config = {
#     "temperature": 1,
#     "top_p": 0.95,
#     "top_k": 64,
#     "max_output_tokens": 8192,
#     "response_mime_type": "text/plain",
# }

# try:
#     model = genai.GenerativeModel(
#         model_name="gemini-1.5-flash",
#         generation_config=generation_config
#     )
# except Exception as e:
#     os.error(f"Failed to load model: {str(e)}")


# @app.route('/')
# def index():
#     return render_template('./templates/profile.html')


# @app.route('/', methods=['POST'])
# def submit():
#     user_answer = request.form.get('answer')
#     place = request.form.get('destination')


#     if user_answer == 'YES':
#                 try:
#                     # Start chat session and send the message
#                     chat_session = model.start_chat(history=[{"role": "user", "parts": [{"text": f"{user_answer}"}]}])
#                     response = chat_session.send_message(f"Please provide travel criteria for {place}, including the best time to visit, estimated cost, and duration.")
#                     recommendation = response.text.strip()
#                     return render_template('profile.html', sum=recommendation)

#                     # Display the recommendation
#                 except Exception as e:
#                     os.error(f"An error occurred while generating criteria")
#     else:
#         return render_template('profile.html', sum="Thank you")



# if __name__ == '__main__':
#     app.run(debug=True)