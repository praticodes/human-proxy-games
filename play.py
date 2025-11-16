import asyncio
import json
import os
import random

from dotenv import load_dotenv

from agents.agent import Agent
from agents.random_agent import RandomAgent
from ah2ac2.baselines.bc_eval import AgentSpecification as BCAgentSpecification
from ah2ac2.baselines.br_bc_eval import AgentSpecification as BRBCAgentSpecification
from ah2ac2.evaluation.evaluation_environment import EvaluationEnvironment
from ah2ac2.evaluation.evaluation_space import EvaluationSpace

load_dotenv()

_TEST_API_KEY = os.getenv("TEST_API_KEY")

with open("action_descriptions.json", "r") as f:
    ACTION_DESCRIPTIONS = json.load(f)


async def play_game(env: EvaluationEnvironment, agent: Agent, agent_type: str, history_file: str = None):
    """
    Plays a single game of Hanabi using the inputted controlled agent and optionally saves all moves to a history file,
    if specified.

    Args:
        env: The evaluation environment to play the game in.
        agent: The controlled agent that will play the game with human proxies.
        agent_type: The type of agent being used.
        history_file: The path to the file to save the game history to.

    Raises:
        Exception: If an error occurs during the game.

    Authors:
        - AH2AC2 Team: ah2ac2@proton.me
        - Hanabi Evaluation Subgroup at the University of Toronto (repository authors).
    """
    try:
        # Get a clean set of initial observations and legal moves
        observations, legal_moves = await env.reset()
        print(legal_moves)
        print(f"Game started. ID: {env.info.game_id}, Controlling: {env.info.candidate_controlling}")

        if history_file:
            with open(history_file, "w") as f:
                f.write(f"Hanabi 3P Game with {agent_type} Agent\n")
                f.write(f"Game ID: {env.info.game_id}\n")
                f.write(f"Controlling: {env.info.candidate_controlling}\n")

        # Assign agent to the role defined in env.info.candidate_controlling
        my_agent = {env.info.candidate_controlling[0]: agent}

        done = False
        current_score = 0.0

        while not done:
            actions_to_send = {}
            for agent_id in env.info.candidate_controlling:
                obs_for_agent = observations[agent_id]
                legal_moves_for_agent = legal_moves[agent_id]

                # Get action from our specific agent instance
                action, my_agent[agent_id] = my_agent[agent_id].act(obs_for_agent, legal_moves_for_agent)
                actions_to_send[agent_id] = action

                if history_file:
                    with open(history_file, "a") as f:
                        f.write(f"Agent {agent_id} took action: {action} ({ACTION_DESCRIPTIONS[action]})\n")

            # Send actions and get the next state
            observations, current_score, done, legal_moves = await env.step(actions_to_send)
            print(f"Step taken. Score: {current_score}, Done: {done}")

        print(f"Game ID {env.info.game_id} finished. Final score: {current_score}")
        if history_file:
            with open(history_file, "a") as f:
                f.write(f"Final score: {current_score}\n")

    except Exception as e:
        print(f"Error during game {env.info.game_id if env._info else 'Unknown'}: {e}")

if __name__ == "__main__":
    # Initialize a test evaluation space
    eval_space_test = EvaluationSpace(_TEST_API_KEY)

    # Randomly determine a play position for our controlled agent
    agent_positions = [0, 1, 2]
    agent_position = random.choice(agent_positions)

    # Create a three-player test environment with the specified agent position
    test_env_3p: EvaluationEnvironment = eval_space_test.new_test_environment(
        num_players=3,
        candidate_position=[agent_position]
    )

    # Prompt user to select an agent
    agent_to_play = None
    agent_type = ""

    # Set controlled agent as per user's choice
    while agent_to_play is None:

        # Prompt user for agent selection
        print("Select an agent to play with:")
        print("1: Random Agent")
        print("2: Behavioral Cloning Baseline Agent")
        print("3: Best Response Behavioral Cloning Agent")
        choice = input("Enter your choice (1, 2, or 3): ")

        # Save and initialize user choice
        if choice == "1":
            agent_to_play = RandomAgent()
            agent_type = "Random"
        elif choice == "2":
            agent_spec = BCAgentSpecification(
                "BC-1k-3p",
                "../models/bc_1k/epoch22_seed0_valacc0.397_3p"
            )
            agent_to_play = agent_spec.init_agent()
            agent_type = "Behavioral Cloning"
        elif choice == "3":
            agent_spec = BRBCAgentSpecification(
                "BR-BC-1k-3p",
                "../models/br_bc_1k/seed0_step76292_3p",
                num_players=3
            )
            agent_to_play = agent_spec.init_agent()
            agent_type = "Best Response Behavioral Cloning"

        else:
            print("Invalid choice. Please try again.")

    # Define the history file path
    history_file_path = os.path.join("game_logs", "game_history.txt")

    # Play the game!
    asyncio.run(play_game(test_env_3p, agent_to_play, agent_type, history_file_path))