#!/usr/bin/python3
import cmd
import sys
import models
import re
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
   
    prompt = '(hbnb) '
    storage = models.storage
    
    classes = {
        "BaseModel": BaseModel,
        # add other classes here
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

    def do_create(self, line):
        if not line:
            print("** class name missing **")
            return

        class_name = line.split()[0]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        new_instance = self.classes[class_name]()
        new_instance.save()
        print(new_instance.id)


    def do_show(self, argv):
        """Prints the string representation of an instance based
        on the class name and id"""
        if not argv:
            print("** class name missing **")
            return

        arg_list = argv.split()
        if len(arg_list) < 2:
            print("** instance id missing **")
            return

        class_name, instance_id = arg_list[0], arg_list[1]
        if class_name not in self.classes:
            print("** class doesn't exist **")
            return

        all_instances = models.storage.all()
        key = class_name + "." + instance_id
        if key not in all_instances:
            print("** no instance found **")
            return
        print(all_instances[key])

    
    def do_destroy(self, argv):
        """Delete a class instance based on the name and given id."""
        arg_list = self.check_args(argv)
        if arg_list:
            if len(arg_list) == 1:
                print("** instance id missing **")
            else:
                key = "{}.{}".format(*arg_list)
                if key in self.storage.all():
                    del self.storage.all()[key]
                    self.storage.save()
                else:
                    print("** no instance found **")


    
    def do_all(self, args):
        """Prints all string representation of all instances based on the class name"""
        all_instances = models.storage.all()
        if args:
            if args not in self.classes:
                print("** class doesn't exist **")
                return
            class_name = args
            instances = [str(val) for key, val in all_instances.items() if key.startswith(class_name + ".")]
        else:
            instances = [str(val) for key, val in all_instances.items()]
        print(instances)

    def do_update(self, line):
        args = self.check_args(line)
        if len(args) < 4:
            print("** instance id, attribute name and value missing **")
        else:
            class_name = args[0]
            instance_id = args[1]
            attribute_name = args[2]
            attribute_value = args[3]

            instance = self.storage.all().get(f"{class_name}.{instance_id}")
            if not instance:
                print("** no instance found **")
            else:
                if not hasattr(instance, attribute_name):
                    setattr(instance, attribute_name, attribute_value)
                else:
                    attr_type = type(getattr(instance, attribute_name))
                    setattr(instance, attribute_name, attr_type(attribute_value))
                self.storage.save()





if __name__ == '__main__':
    HBNBCommand().cmdloop()
    