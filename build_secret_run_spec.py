entries = [ 

    # Misc datasets
    {'scenario': 'summarization', 'description': "sam_sum:model=neurips/local", 'priority': 1},
    {'scenario': 'causation', 'description': "corr2cause:model=neurips/local,max_train_instances=1",'priority': 1},

    ## Ethics datasets
    {'scenario': 'ethics', 'description': "ethics_justice:model=neurips/local", 'priority': 1},
    {'scenario': 'ethics', 'description': "ethics_commonsense:model=neurips/local", 'priority': 1},
    {'scenario': 'ethics', 'description': "ethics_virtue:model=neurips/local", 'priority': 1},
    {'scenario': 'ethics', 'description': "ethics_deontology:model=neurips/local", 'priority': 1},
    {'scenario': 'ethics', 'description': "ethics_utilitarianism:model=neurips/local", 'priority': 1},

    ## Math datasets
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=1,use_official_examples=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=1,use_official_examples=True", 'priority': 2},
# 
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=2,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=2,use_official_examples=True", 'priority': 4},
# 
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=3,use_official_examples=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=3,use_official_examples=True", 'priority': 2},
# 
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=4,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=4,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=4,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=4,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=4,use_official_examples=True", 'priority': 4},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=4,use_official_examples=True", 'priority': 4},
#    {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=4,use_official_examples=True", 'priority': 4},

    {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=5,use_official_examples=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=5,use_official_examples=True", 'priority': 2},

    # With chain-of-thought prompting:
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=1,use_chain_of_thought=True", 'priority': 2},
     {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=1,use_chain_of_thought=True", 'priority' : 2},
# 
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=3,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=3 ,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=3,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=3,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=3,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=3,use_chain_of_thought=True", 'priority': 2},
#     {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=3,use_chain_of_thought=True", 'priority' : 2},
# 
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=number_theory,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=intermediate_algebra,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=algebra,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=prealgebra,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=geometry,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=counting_and_probability,level=5,use_chain_of_thought=True", 'priority': 2},
    {'scenario': 'math', 'description': "math:model=neurips/local,subject=precalculus,level=5,use_chain_of_thought=True", 'priority' : 2},

    {'scenario':'cnn','description': "summarization_cnndm:model=neurips/local", 'priority': 1},

]



def generate_equal_sum_list(V, N):
    # Calculate the base value that will be repeated.
    base_value = V // N
    # Calculate the remainder for distribution.
    remainder = V % N
    
    # Create the list with base_value repeated N times.
    result = [base_value] * N
    
    # Distribute the remainder evenly among the elements.
    for i in range(remainder):
        result[i] += 1
    
    return result

import pandas as pd
import argparse

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(
        description='''
        This method automatically generates a configuration file for the neurips_llm_efficiency_challenge
        
        Calling it with: `python build_run_specs_full.py --example_budget=600` will produce a conf file 
        with a total of 600 examples distributed evenly across scenarios as also defined here.
        ''',
    )
    parser.add_argument("--example_budget", required=True, type=int, help='# example to use')
    args = parser.parse_args()
    
    # get a list of scenarios and n_examples
    df =  pd.DataFrame(entries)
    scenario_count_dict = df.value_counts('scenario').to_dict()
    n_scenarios = len(df.scenario.unique())
    max_eval_instances_per_scenario = generate_equal_sum_list(args.example_budget, n_scenarios)

    # get a dict of the amount of examples per 
    scenario_n_examples_dict = {}
    for scenario, n_subscenarios in scenario_count_dict.items():
        cur_max_eval_instances_per_scenario = max_eval_instances_per_scenario.pop()
        scenario_n_examples_dict[scenario] = generate_equal_sum_list(cur_max_eval_instances_per_scenario,n_subscenarios)

    for i in range(len(entries)):
        cur_scenario = entries[i]['scenario']
        # print(f"added {v} to {entries[i]['max_eval_instances']}")
        v = scenario_n_examples_dict[cur_scenario].pop()
        entries[i]['max_eval_instances'] = v

    with open(f'./run_specs_full_closed_eval_coarse_{args.example_budget}_budget.conf','w') as f:
        f.write('entries: [\n')
        last_scenario = ''
        for entry in entries:
            cur_scenario = entry['scenario']
            if cur_scenario != last_scenario:
                f.write(f'\n# {cur_scenario}\n')
                print(entry)
            last_scenario = cur_scenario
            f.write('{')
            f.write(f'description: """{entry["description"]}'.replace('"""','"'))
            f.write(f',max_eval_instances={entry["max_eval_instances"]}""",priority: 1'.replace('"""','"'))
            f.write('}\n')
        f.write(']')

    print(f'Saved ./run_secret_specs_full_coarse_{args.example_budget}_budget.conf')
