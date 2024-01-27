import openai
import time

# Set your OpenAI GPT-3 API key
openai.api_key = 'OPENAI-API-KEY'

# Function to check vulgarity and generate alternative using GPT-3
def process_sentence(input_sentence, max_retries=5):
    retries = 0

    while retries < max_retries:
        try:
            # Check if input_sentence contains vulgarity
            if contains_vulgarity(input_sentence):
                # Use GPT-3 to generate an alternative sentence
                alternative_sentence = generate_alternative(input_sentence)
                return alternative_sentence
            else:
                return input_sentence
        except openai.error.RateLimitError as e:
            print(f"Rate limit reached: {e}")
            print(f"Waiting for 60 seconds before retrying (attempt {retries + 1}/{max_retries})...")
            time.sleep(60)  # Wait for 60 seconds
            print("Retrying...")
            retries += 1
        except openai.error.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

    print("Max retries reached. Could not process the sentence.")
    return None

# Function to check vulgarity and generate alternative using GPT-3
def process_sentence(input_sentence):
    # Check if input_sentence contains vulgarity
    if contains_vulgarity(input_sentence):
        # Use GPT-3 to generate an alternative sentence
        alternative_sentence = generate_alternative(input_sentence)
        return alternative_sentence
    else:
        return input_sentence

# Function to check vulgarity
def contains_vulgarity(sentence):
    # Set up parameters for the GPT-3 API call
    prompt = f"Is the following sentence inappropriate?  '{sentence}'"

    # Make an API call to GPT-3 with the updated model
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Use a currently supported model
        prompt=prompt,
        max_tokens=50  # Adjust as needed
    )

    # Extract the generated response from GPT-3
    gpt3_response = response['choices'][0]['text'].strip()

    # Analyze the content of the response for vulgarity indication
    if "yes" in gpt3_response.lower():
        return True
    else:
        return False

# Function to generate alternative sentence using GPT-3
def generate_alternative(input_sentence):
    # Set up parameters for the GPT-3 API call
    prompt = f"Given the sentence: '{input_sentence}', provide an appropriate alternative:"

    # Make an API call to GPT-3
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",  # Choose the engine based on your needs
        prompt=prompt,
        max_tokens=100  # Adjust as needed
    )

    # Extract the generated alternative sentence from the GPT-3 response
    alternative_sentence =  response['choices'][0]['text'].strip()
    return alternative_sentence

# Example usage
user_input = "i dont give two fucks about you"

try:
    processed_input = process_sentence(user_input)
    print(processed_input)
except openai.error.RateLimitError as e:
    print(f"Rate limit reached: {e}")
    print("Waiting for 60 seconds before retrying...")
    time.sleep(60)  # Wait for 60 seconds
    print("Retrying...")
    processed_input_retry = process_sentence(user_input)
    print(processed_input_retry)
