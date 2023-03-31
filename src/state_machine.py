
import time
import json

# FILE SETTINGS ----------------------------------------------|
FILE_NAME = "missionStates"
PATH = f"./{FILE_NAME}.json"
PI_PATH = f"/home/pi/{FILE_NAME}.json"

class States:

    CURRENT = "CurrentState"
    PREDEPLOYMENT = "Predeployment"
    DEPLOYMENT = "Deployment"
    MISSION = "Mission"

    PREDEPLOYMENT_SUBS = {
        "Rail": True,
        "Ascent": False,
        "Descent": False,
        "Land": False,
    }

    DEPLOYMENT_SUBS = {
        "Dirtbrake": False,
        "Bay": False,
        "Arm": False,
        "Gimbal": False,
    }

    MISSION_SUBS = {
        "Execution": False,
        "Completion": False,
    }


class StateMachine:

    def __init__(self, path: str) -> None:
        self.json = path
    
    def setNewState(self, state: str, substates: dict) -> None:
        """Sets a new state.
        
        Args:
            state(str): the name of the state.
            substates(dict): the full set of substates.
        """
        state = {
            States.CURRENT: state,
            state: substates,
        }
        with open(self.json, "w") as output:
            json.dump(state, output, indent=4)

    def updateState(self, state: str, substate: str, status: bool) -> None:
        """Updates a given state in the current state.
        
        Args:
            state(str): the current state.
            subState(str): the substate in the current state to update.
            status(bool): the value to update the desired substate to.
        """
        with open(self.json, "r+") as source:
            state_machine = json.load(source)
            state_machine[state][substate] = status
            source.seek(0)
            json.dump(state_machine, source, indent=4)
            source.truncate()
    
    def getState(self) -> str:
        """Gets the current state.

        Returns:
            string: the current state.
        """
        with open(self.json, "r") as source:
            state = json.load(source)[States.CURRENT]
        return state
    
    def getSubstate(self) -> str:
        """Gets the last substate in the current state with a status of true.

        Returns:
            str: the string description of the current substate
        """
        with open(self.json, "r") as source:
            state_machine = json.load(source)
            current = state_machine[state_machine["CurrentState"]]
            for state in reversed(current.keys()):
                if current[state]:
                    break
        return state
    
    def __str__(self) -> str:
        with open(self.json, "r") as source:
            dict = json.load(source)
        return f"{dict}"

if __name__ == "__main__":
    def printStats(states):
        print(states.getState())
        print(states.getSubstate())
        print(states)
    '''
    states = StateMachine(PATH)
    states.setNewState(States.PREDEPLOYMENT, States.PREDEPLOYMENT_SUBS)
    printStats(states)
    
    states.updateState(States.PREDEPLOYMENT, "Land", True)
    printStats(states)

    states.updateState(States.PREDEPLOYMENT, "Land", False)
    states.updateState(States.PREDEPLOYMENT, "Ascent", True)
    printStats(states)

    states.setNewState(States.DEPLOYMENT, States.DEPLOYMENT_SUBS)
    printStats(states)
    '''
    states = StateMachine(PATH)
    printStats(states)