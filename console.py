#!/usr/bin/python3
import cmd
import sys
import models
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage

class HBNBCommand(cmd.Cmd):
   
    prompt = '(hbnb) '
    storage = models.storage
    
    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review,
    }

    
    def check_args(self, line):
        return [arg.strip('"') for arg in re.findall(r'\b(".+?"|\S+)\b', line)]


    
    def emptyline(self):
        """Command to executed when empty line + <ENTER> key"""
        pass


    def do_quit(self, args):
        """Quit command to exit the program"""
        return True


    def do_EOF(self, args):
        """EOF command to exit the program"""
        return True


    def do_create(self, argv):
        """Create a new instance of BaseModel, saves it (to the JSON file) and prints the id"""
        if len(argv) == 0:
            print("** class name missing **")
        else:
            arg_list = self.check_args(argv)
            if arg_list[0] == "BaseModel":
                new_obj = BaseModel()
            elif arg_list[0] == "User":
                new_obj = User()
            new_obj.save()
            print(new_obj.id)


    def do_show(self, argv):
        """Shows an instance based on the class name and id."""
        arg_list = self.check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** class name missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    print(self.storage.all()[key])
                else:
                    print("** no instance found **")


   
    def do_destroy(self, argv):
        """Delete a class instance based on the name and given id."""
        arg_list = self.check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                class_name = arg_list[0]
                obj_id = arg_list[1]
                key = "{}.{}".format(class_name, obj_id)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")


    
    def do_all(self, argv):
        """Prints all string representation of all instances based or not on the class name."""
        arg_list = self.check_args(argv)
        if len(arg_list) == 0:
            for key, value in self.storage.all().items():
                print(value)
        elif len(arg_list) == 1:
            if arg_list[0] in ["BaseModel", "User"]:
                for key, value in self.storage.all().items():
                    if type(value).__name__ == arg_list[0]:
                        print(value)
            else:
                print("** class doesn't exist **")
                
        else:
            print("** class name missing **")


    def do_update(self, argv):
        """Updates an instance based on the class name and id by adding or updating attribute (save the change into the JSON file)."""
        arg_list = self.check_args(argv)
        if len(arg_list) == 0:
            print("** class name missing **")
        elif len(arg_list) == 1:
            print("** instance id missing **")
        elif len(arg_list) == 2:
            print("** attribute name missing **")
        elif len(arg_list) == 3:
            print("** value missing **")
        else:
            key = "{}.{}".format(arg_list[0], arg_list[1])
            if key in self.storage.all():
                if hasattr(self.storage.all()[key], arg_list[2]):
                    setattr(self.storage.all()[key], arg_list[2], arg_list[3])
                    self.storage.all()[key].save()
                else:
                    print("** no attribute found **")
            else:
                print("** no instance found **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
    