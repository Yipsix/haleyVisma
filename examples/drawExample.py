import face_recognition
from PIL import Image, ImageDraw, ImageFont


anders_image = face_recognition.load_image_file("pictures/Martin.jpg")
anders_face_encoding = face_recognition.face_encodings(anders_image)[0]

jesper_image = face_recognition.load_image_file("pictures/Jesper.jpg")
jesper_face_encoding = face_recognition.face_encodings(jesper_image)[0]

per_image = face_recognition.load_image_file("pictures/Per.jpg")
per_face_encoding = face_recognition.face_encodings(per_image)[0]

known_face_encodings = [
    anders_face_encoding,
    jesper_face_encoding,
    per_face_encoding
]
known_face_names = [
    "Martin",
    "Jesper",
    "Per"
]

unknown_image = face_recognition.load_image_file("pictures/persons.jpg")

face_locations = face_recognition.face_locations(unknown_image)
face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

pil_image = Image.fromarray(unknown_image)

draw = ImageDraw.Draw(pil_image)

# get a font
fnt = ImageFont.truetype('FreeMono.ttf', 40)

for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    name = "Unknown"

    if True in matches:
        first_match_index = matches.index(True)
        name = known_face_names[first_match_index]

    draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))

    text_width , text_height = draw.textsize(name) 
    draw.rectangle(((left, bottom - text_height - 40), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
    draw.text((left + 6, bottom - text_height  - 30), name, font=fnt, fill=(255, 255, 255, 255))


del draw

pil_image.show()