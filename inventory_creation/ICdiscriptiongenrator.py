import base64
from openai import OpenAI
import inventory_creation.ICsystem_prompts as ICsystem_prompts
from dotenv import load_dotenv
import os


def write_Discription_for_fashion( title , img_path ):

    load_dotenv()
    api_key=os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    
    response=process_image_with_openai(image_path=img_path,description=title,prompt=ICsystem_prompts.DiscriptionGenrator,client=client)
    return response
    
def write_Discription_for_artandcraft( title , img_path ):
    
    load_dotenv()
    api_key=os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    
    response=process_image_with_openai(image_path=img_path,description=title,prompt=ICsystem_prompts.ArtAndCraftDescriptionGenerator,client=client)
    return response

def write_Discription_for_Packed_food( title , img_path ):
    
    load_dotenv()
    api_key=os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    
    response=process_image_with_openai(image_path=img_path,description=title,prompt=ICsystem_prompts.pakedfoodDescriptionGenerator,client=client)
    return response

def write_Discription_for_sweets_and_snacks( title , img_path ):
    
    load_dotenv()
    api_key=os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)
    
    response=process_image_with_openai(image_path=img_path,description=title,prompt=ICsystem_prompts.SweetsDescriptionGenerator,client=client)
    return response


def process_image_with_openai(image_path, description, prompt, client, model="gpt-4o-mini"):
    """
    Process an image using OpenAI's API
    
    Args:
        image_path (str): Path to the image file
        description (str): Description of the image
        prompt (str): The prompt to send to the API
        client: OpenAI client instance
        model (str): Model to use for processing (default: "gpt-4o-mini")
    
    Returns:
        dict: The API response
    """
    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    
    # Get base64 encoded image
    base64_image = encode_image(image_path)
    
    # Create API request
    response = client.chat.completions.create(
        model=model,
        messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt+description,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                },
            ],
        }
    ],
)
    
    return response.choices[0].message.content
# Example usage
if __name__ == "__main__":
    
    response=write_Discription_for_fashion(img_path="D:\DEV\ONDC\CarterONDC\img.jpg",title="tshirt")
    
    print(response)
