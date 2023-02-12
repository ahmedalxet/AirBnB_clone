import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)"""
        with open(FileStorage.__file_path, mode='w', encoding='utf-8') as file:
            obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
            json.dump(obj_dict, file)

    def reload(self):
        """Deserialize the JSON file to __objects (only if the JSON file (__file_path) exists ; otherwise, do nothing. If the file doesn’t exist, no exception should be raised)"""
        try:
            with open(FileStorage.__file_path, mode='r', encoding='utf-8') as file:
                for key, value in json.load(file).items():
                    class_name = value.get("__class__")
                    if class_name == "BaseModel":
                        FileStorage.__objects[key] = BaseModel(**value)
                    elif class_name == "User":
                        FileStorage.__objects[key] = User(**value)
                    elif class_name == "State":
                        FileStorage.__objects[key] = State(**value)
                    elif class_name == "City":
                        FileStorage.__objects[key] = City(**value)
                    elif class_name == "Amenity":
                        FileStorage.__objects[key] = Amenity(**value)
                    elif class_name == "Place":
                        FileStorage.__objects[key] = Place(**value)
                    elif class_name == "Review":
                        FileStorage.__objects[key] = Review(**value)
        except FileNotFoundError:
            pass
