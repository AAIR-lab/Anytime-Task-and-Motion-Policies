from Wrappers.ArgumentV2 import ArgumentV2
from LLActionSpecV2 import LLActionSpecV2
from Wrappers.Effect import Effect
import json
from Precondition.Precondition import Precondition
from Predicates.Predicate import Predicate
from Predicates.NotObstructs import NotObstructs
from Predicates.IsBigger import IsBigger
from Predicates.isMotionPlan import isMotionPlan
from Predicates.NotPutdownObstructs import NotPutdownObstructs
from Predicates.BatterySufficient import BatterySufficient
from Predicates.IsBatterySufficient import IsBatterySufficient


class ActionConfigParserV2(object):
    def __init__(self, action_config_file):
        self.parse(action_config_file)

    def parse(self, action_config_file):
        with open(action_config_file) as f:
            self.action_config = json.load(f)

        self.__action_obj_map = self.__parse_ll_action_specs()

    def get_actions(self):
        return self.__action_obj_map.keys()

    def get_ignore_action_list(self):
        return self.action_config.get('ignore_hl_actions', None)

    def get_non_removable_bodies(self):
        return self.action_config.get('non_removable_bodies', None)

    def get_specification(self, action):
        return self.__action_obj_map.get(action)

    def __parse_ll_action_specs(self):
        action_obj_map = {}
        config_map = self.action_config.get('config_map', None)
        for action in config_map:
            action_spec = config_map[action]
            action_obj = self.__parse_action(action, action_spec)
            action_obj_map[action] = action_obj

        return action_obj_map

    def __parse_action(self, action_name, action_spec_map):
        print "Parsing Action :" + action_name
        precondition_predicates = self.__parse_predicates(action_spec_map.get('precondition', None), action_spec_map.get('LL_ARGS', None))
        precondition = Precondition(precondition_predicates)
        effect_predicates = self.__parse_predicates(action_spec_map.get('effect', None), action_spec_map.get('LL_ARGS', None))
        effect = Effect(effect_predicates)
        exec_sequence = action_spec_map.get("execution_sequence",None)
        attach_obj = action_spec_map.get("attach",None)
        hl_args = action_spec_map.get("HL_ARGS",None)
        print "Going Back"
        return LLActionSpecV2(action_name, precondition, effect, updates_ll_state=action_spec_map.get('updates_ll_state', False),execution_sequence=exec_sequence,attach= attach_obj,hl_args=hl_args)

    def __parse_predicates(self, predicates, ll_args):
        '''Returns a list of predicate objects'''
        predicate_obj_list = []
        for predicate in predicates:
            assert ('(' in predicate), "Invalid predicate :" + predicate

            arg_object_list = None
            open_paren_index = predicate.index('(')
            predicate_name = predicate[0:open_paren_index]
            # print "\tPredicate: "+predicate_name
            args = predicate[open_paren_index + 1:predicate.index(')')].split(',')
            for argument_name in args:
                # print "\t\tArgument: " + argument_name

                argument_name = argument_name.strip(' ')
                argument_name_alias = None
                if ':' in argument_name:
                    left, right = argument_name.split(':')
                    argument_name = left
                    argument_name_alias = right
                    arg_type = "alias"
                    generator_class = None
                else:
                    arg_details = ll_args[argument_name]
                    if len(arg_details) > 0:
                        generator_class = arg_details[0]
                        arg_type = arg_details[1]
                    else:
                        generator_class = None
                        arg_type = "hl_arg"
                arg_obj = ArgumentV2(argument_name,
                                    arg_type=arg_type,
                                    generator_class_name=generator_class,
                                    name_alias = argument_name_alias
                                     )
                if arg_object_list is None:
                    arg_object_list = []
                arg_object_list.append(arg_obj)
            # Check if the predicate has be custom defined:
            predicate_obj = None
            try:
                predicate_obj = globals().get(predicate_name)(predicate_name, arg_object_list)
            except:
                predicate_obj = Predicate(predicate_name, arg_object_list)



            predicate_obj_list.append(predicate_obj)
        return predicate_obj_list

if __name__ == "__main__":
    acpv2 = ActionConfigParserV2('/home/midhun/Documents/TMP_Merged/ActionConfigV2')
    print acpv2.get_actions()
    spec = acpv2.get_specification('grasp')
    print spec
