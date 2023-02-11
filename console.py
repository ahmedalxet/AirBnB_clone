import cmd
import models

class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, args):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered"""
        pass

    def do_help(self, args):
        """List available commands with 'help' or detailed help with 'help cmd'."""
        if args:
            try:
                doc = getattr(self, 'do_' + args).__doc__
                if doc:
                    print(doc)
                else:
                    print("No documentation found for '%s'" % args)
            except AttributeError:
                print("No command '%s' found" % args)
        else:
            names = [name.split('_', 1)[1] for name in dir(self) if name.startswith('do_')]
            names.sort()
            print("Available commands:", ', '.join(names))

    def do_create(self, args):
        """Create a new instance of a class and save it to storage"""
        if not args:
            print("** class name missing **")
        else:
            class_name = args
            new_obj = models.BaseModel()
            models.storage.new(new_obj)
            models.storage.save()
            print(new_obj.id)

    def do_show(self, args):
        """Print an instance of a class by id"""
        if not args:
            print("** class name missing **")
        else:
            class_name, obj_id = args.split()
            key = "{}.{}".format(class_name, obj_id)
            obj = models.storage.all().get(key)
            if obj:
                print(obj)
            else:
                print("** no instance found **")

    def do_destroy(self, args):
        """Delete an instance of a class by id"""
        if not args:
            print("** class name missing **")
        else:
            class_name, obj_id = args.split()
            key = "{}.{}".format(class_name, obj_id)
            obj = models.storage.all().get(key)
            if obj:
                del models.storage.all()[key]
                models.storage.save()
            else:
                print("** no instance found **")

