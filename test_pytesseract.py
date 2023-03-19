# from PIL import Image
# import os

# # Define the path to the image file
# file_path = os.path.join(os.getcwd(), 'cogs', 'temp', 'karuta_drop.jpg')

# # Open the image file and crop the four cards
# img = Image.open(file_path)
# top = 65
# bottom = 103
# card1 = img.crop((50, top, 230, bottom))
# card2 = img.crop((320, top, 505, bottom))
# card3 = img.crop((600, top, 780, bottom))
# card4 = img.crop((870, top, 1050, bottom))

# # Define the path to the directory where you want to save the files
# output_dir = os.path.join(os.getcwd(), 'cogs', 'temp')

# # Create the directory if it doesn't already exist
# if not os.path.exists(file_path):
#     os.makedirs(file_path)

# # Save each card as a separate JPEG file in the output directory
# card1.convert('RGB').save(os.path.join(output_dir, 'card1.jpg'))
# card2.convert('RGB').save(os.path.join(output_dir, 'card2.jpg'))
# card3.convert('RGB').save(os.path.join(output_dir, 'card3.jpg'))
# card4.convert('RGB').save(os.path.join(output_dir, 'card4.jpg'))
