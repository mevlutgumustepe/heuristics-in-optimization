import random 
import time

# dataset = "JACKSON.IN2"
# cycle_time = 10

dataset_cycleTime = [
    {
        "dataset" : "JACKSON.IN2",
        "cycle_time" : 10
    },
    {
        "dataset" : "JACKSON.IN2",
        "cycle_time" : 19
    },
    {
        "dataset" : "KILBRID.IN2",
        "cycle_time" : 56
    },
    {
        "dataset" : "KILBRID.IN2",
        "cycle_time" : 150
    },
    {
        "dataset" : "TONGE70.IN2",
        "cycle_time" : 250
    },
    {
        "dataset" : "TONGE70.IN2",
        "cycle_time" : 600
    },
    {
        "dataset" : "ARC83.IN2",
        "cycle_time" : 3786
    },
    {
        "dataset" : "ARC83.IN2",
        "cycle_time" : 9000
    }
]



repeat = 100


def longest_and_local(dataset, cycle_time, repeat):

    print("DATASET : " + dataset)
    print("CYCLE TIME : " + str(cycle_time))
    print("REPEAT COUNT : " + str(repeat))


    def longest_task_time(dN, cT): 
        ##### dN represents the dataset
        ##### cT represents the cycle time
        
        cycleTime = cT

        usable_data = [] ##### to transform row data to usable data an empty array is assigned

        ##### data reading process
        with open(dN) as readed_data:
            d = readed_data.readlines()
            for i in range(len(d)-1): ##### if the line value equals -1,-1 the reading stops since it represents the last line
                usable_data.append(d[i][:-1])

        # first line of data is task number
        task_count = int(usable_data[0])

        # task count number of lines after the first line represents task times
        task_times = [int(usable_data[i]) for i in range(1, task_count+1)]

        feasibility = True
        for i in task_times: 
            if i > cycleTime: feasibility: False

        if feasibility == False: print("NOT FEASIBLE")
        else:  

            # after the task times the have precedence relationships
            precedessor_list = []

            for j in range(1,task_count+1):
                
                precedessors_of_task = []

                for i in range(task_count+1, len(usable_data)):

                    # presedence is p, successor is s in data
                    p,s = usable_data[i].split(",")
                    if int(j) == int(s) : precedessors_of_task.append(int(p))
                
                precedessor_list.append(precedessors_of_task)
            
            
            ##### to detect starting tasks following array will be used
            ##### if a task do not have any precedessor it will be starting task
            ##### there can be more than one starting tasks depends on the precedessors
            starting_tasks = [i+1 for i in range(len(precedessor_list)) if precedessor_list[i] == []]

            best_solution = {} ##### as an initialization best solution is None
            best_num_of_stations = float('inf') ##### best number of stations is set to infinity for initialization


            completed_tasks = [] ##### completed_tasks set to an empty array at each iteration

            ##### at beginning only starting tasks available and can be chosen
            ##### later, available tasks will be determined according to completion status of precedessors of a task
            available_tasks = starting_tasks.copy() 

            station_count = 1 ##### like an id of a station

            station_tasks = [] ##### the tasks that are included in station
            station_capacity = 0 ##### station capacity set 0 since there is no task at the beginning

            solution = {} ##### the stations will be saved here

            ##### the following while loop works until all the tasks are completed
            while len(completed_tasks) != task_count: 

                max_task_time = 0

                assigned = None

                for i in available_tasks: 
                    if task_times[i-1] >= max_task_time:
                        assigned = i
                        max_task_time = task_times[i-1]
                
                if station_capacity + task_times[assigned-1] > cT:
                    max_task_time = 0
                    for i in available_tasks: 
                        if task_times[i-1] >= max_task_time and task_times[assigned-1] + station_capacity <= cT:
                            assigned = i
                            max_task_time = task_times[i-1]
                
                def addToCurrentStation() : 

                    nonlocal station_capacity
                    nonlocal station_tasks
                    nonlocal completed_tasks
                    nonlocal task_times
                    nonlocal assigned
                    nonlocal task_count
                    nonlocal available_tasks

                    station_tasks.append(assigned) ##### assigned task assigned to current station
                    completed_tasks.append(assigned) ##### assigned tasks added to completed tasks
                    station_capacity += task_times[assigned-1] ##### station capacity increased as task time of assigned task

                    available_tasks.clear() ##### for the following available tasks, available tasks array cleared
                    for i in range(1, task_count+1):
                        ##### if all precedessors are done task added to available tasks array
                        is_all_precedessors_completed = True
                        for j in precedessor_list[i-1]: 
                            if j!=[]:
                                if j not in completed_tasks: is_all_precedessors_completed = False
                        if is_all_precedessors_completed == True and i not in completed_tasks: available_tasks.append(i)


                def openNewStation():

                    nonlocal solution
                    nonlocal station_count
                    nonlocal station_tasks
                    nonlocal station_capacity
                    nonlocal station_count
                    nonlocal assigned
                    nonlocal available_tasks
                    nonlocal completed_tasks

                    ##### current station will be added to solution
                    solution[str(station_count)] = station_tasks.copy()
                    ##### clear station capacity and tasks
                    station_tasks.clear()
                    station_capacity = 0
                    ##### opening new station
                    station_count += 1
                    ##### adding assigned station's task time to station capacity and station tasks
                    station_tasks.append(assigned)
                    completed_tasks.append(assigned)
                    station_capacity += task_times[assigned-1]

                    available_tasks.clear() ##### for the following available tasks, available tasks array cleared
                    for i in range(1, task_count+1):
                        ##### if all precedessors are done task added to available tasks array
                        is_all_precedessors_completed = True
                        for j in precedessor_list[i-1]: 
                            if j!=[]:
                                if j not in completed_tasks: is_all_precedessors_completed = False
                        if is_all_precedessors_completed == True and i not in completed_tasks: available_tasks.append(i)

                
                def addRemainingTasksToStation():
                    
                    nonlocal solution
                    nonlocal station_capacity
                    nonlocal station_tasks
                    nonlocal station_count
                    
                    solution[str(station_count)] = station_tasks.copy()
                    ##### clear station capacity and tasks
                    station_tasks.clear()
                    station_capacity = 0
                    station_count = 1


                ##### if station capacity is not exceed with the new assigned task
                if station_capacity + task_times[assigned-1] <= cT: addToCurrentStation()
                    
                
                ##### if station capacity exceeded when the assigned task added
                else: openNewStation()
                    
                
                ##### if all tasks are completed last station added to the solution
                if len(completed_tasks) == task_count: addRemainingTasksToStation()
                    
            ##### if better solution found, best solution updated
            if len(solution) <= best_num_of_stations:
                best_num_of_stations = len(solution)
                best_solution = solution

            return best_solution


    def local_search_swap(dN, cT, best_solution, repeat):
        ##### dN represents the dataset
        ##### cT represents the cycle time

        swap_random_values = {}

        for i in best_solution.values():
            for j in i: 
                swap_random_values[str(j)] = (random.randint(1,100))/100

        
        cycleTime = cT

        usable_data = [] ##### to transform row data to usable data an empty array is assigned

        ##### data reading process
        with open(dN) as readed_data:
            d = readed_data.readlines()
            for i in range(len(d)-1): ##### if the line value equals -1,-1 the reading stops since it represents the last line
                usable_data.append(d[i][:-1])

        # first line of data is task number
        task_count = int(usable_data[0])

        # task count number of lines after the first line represents task times
        task_times = [int(usable_data[i]) for i in range(1, task_count+1)]

        feasibility = True
        for i in task_times: 
            if i > cycleTime: feasibility: False

        if feasibility == False: print("NOT FEASIBLE")
        else:  

            # after the task times the have precedence relationships
            precedessor_list = []

            for j in range(1,task_count+1):
                
                precedessors_of_task = []

                for i in range(task_count+1, len(usable_data)):

                    # presedence is p, successor is s in data
                    p,s = usable_data[i].split(",")
                    if int(j) == int(s) : precedessors_of_task.append(int(p))
                
                precedessor_list.append(precedessors_of_task)
            
            
            ##### to detect starting tasks following array will be used
            ##### if a task do not have any precedessor it will be starting task
            ##### there can be more than one starting tasks depends on the precedessors
            starting_tasks = [i+1 for i in range(len(precedessor_list)) if precedessor_list[i] == []]

            ##### count variable holds the iteration count
            count = 0
            ##### there is a limit count which is multiplication of number of tasks and 10

            def doSwapOperation():
                    
                nonlocal task_count
                nonlocal swap_random_values

            
                ind1 = random.randint(1,task_count)
                ind2 = random.randint(1,task_count)
                
                while ind1 == ind2: 
                    ind2 = random.randint(1,task_count)

                val1 = swap_random_values[str(ind1)]
                val2 = swap_random_values[str(ind2)]

                swap_random_values[str(ind2)] = val1
                swap_random_values[str(ind1)] = val2

            while count < task_count * repeat :

                doSwapOperation()

                completed_tasks = [] ##### completed_tasks set to an empty array at each iteration

                ##### at beginning only starting tasks available and can be chosen
                ##### later, available tasks will be determined according to completion status of precedessors of a task
                available_tasks = starting_tasks.copy() 

                station_count = 1 ##### like an id of a station

                station_tasks = [] ##### the tasks that are included in station
                station_capacity = 0 ##### station capacity set 0 since there is no task at the beginning

                solution = {} ##### the stations will be saved here

                ##### the following while loop works until all the tasks are completed
                while len(completed_tasks) != task_count: 

                    swap_value_list = [swap_random_values[str(i)] for i in available_tasks]

                    ##### assigned task is the task at random index
                    assigned = available_tasks[swap_value_list.index(max(swap_value_list))]

                    def addToCurrentStation() : 

                        nonlocal station_capacity
                        nonlocal station_tasks
                        nonlocal completed_tasks
                        nonlocal task_times
                        nonlocal assigned
                        nonlocal task_count
                        nonlocal available_tasks

                        station_tasks.append(assigned) ##### assigned task assigned to current station
                        completed_tasks.append(assigned) ##### assigned tasks added to completed tasks
                        station_capacity += task_times[assigned-1] ##### station capacity increased as task time of assigned task

                        available_tasks.clear() ##### for the following available tasks, available tasks array cleared
                        for i in range(1, task_count+1):
                            ##### if all precedessors are done task added to available tasks array
                            is_all_precedessors_completed = True
                            for j in precedessor_list[i-1]: 
                                if j!=[]:
                                    if j not in completed_tasks: is_all_precedessors_completed = False
                            if is_all_precedessors_completed == True and i not in completed_tasks: available_tasks.append(i)


                    def openNewStation():

                        nonlocal solution
                        nonlocal station_count
                        nonlocal station_tasks
                        nonlocal station_capacity
                        nonlocal station_count
                        nonlocal assigned
                        nonlocal available_tasks
                        nonlocal completed_tasks

                        ##### current station will be added to solution
                        solution[str(station_count)] = station_tasks.copy()
                        ##### clear station capacity and tasks
                        station_tasks.clear()
                        station_capacity = 0
                        ##### opening new station
                        station_count += 1
                        ##### adding assigned station's task time to station capacity and station tasks
                        station_tasks.append(assigned)
                        completed_tasks.append(assigned)
                        station_capacity += task_times[assigned-1]

                        available_tasks.clear() ##### for the following available tasks, available tasks array cleared
                        for i in range(1, task_count+1):
                            ##### if all precedessors are done task added to available tasks array
                            is_all_precedessors_completed = True
                            for j in precedessor_list[i-1]: 
                                if j!=[]:
                                    if j not in completed_tasks: is_all_precedessors_completed = False
                            if is_all_precedessors_completed == True and i not in completed_tasks: available_tasks.append(i)

                    
                    def addRemainingTasksToStation():
                        
                        nonlocal solution
                        nonlocal station_capacity
                        nonlocal station_tasks
                        nonlocal station_count
                        
                        solution[str(station_count)] = station_tasks.copy()
                        ##### clear station capacity and tasks
                        station_tasks.clear()
                        station_capacity = 0
                        station_count = 1


                    ##### if station capacity is not exceed with the new assigned task
                    if station_capacity + task_times[assigned-1] <= cT: addToCurrentStation()
                        
                    
                    ##### if station capacity exceeded when the assigned task added
                    else: openNewStation()
                        
                    
                    ##### if all tasks are completed last station added to the solution
                    if len(completed_tasks) == task_count: addRemainingTasksToStation()
                        
                ##### if better solution found, best solution updated
                if len(solution) <= len(best_solution):
                    best_num_of_stations = len(solution)
                    best_solution = solution

                count += 1

            return best_solution


    print("LONGEST TASK TIME METHOD ***************************** LONGEST TASK TIME METHOD ***************************** LONGEST TASK TIME METHOD")
    time1 = time.time()
    longest_task_time_result = longest_task_time(dN = dataset, cT = cycle_time)
    for i in longest_task_time_result.keys():
        print(f"Station {i} : {longest_task_time_result[i]}")
    print(f"Best number of stations is {len(longest_task_time_result)}.")
    time2 = time.time()
    print("Time Elapsed: " + str(time2-time1) + " seconds")


    print("LOCAL SEARCH WITH LONGEST T.T. RESULT ***************************** LOCAL SEARCH WITH LONGEST T.T. RESULT ***************************** LOCAL SEARCH WITH LONGEST T.T. RESULT")
    time3 = time.time()
    local_best_longest = local_search_swap(dN = dataset, cT = cycle_time, best_solution=longest_task_time_result, repeat = repeat)
    for i in local_best_longest.keys():
        print(f"Station {i} : {local_best_longest[i]}")
    print(f"Best number of stations is {len(local_best_longest)}.")
    time4 = time.time()
    print("Time Elapsed: " + str(time4-time3) + " seconds")


for i in dataset_cycleTime:
    
    longest_and_local(dataset=i["dataset"], cycle_time=i["cycle_time"], repeat=repeat)

    print("-----------------------------------------")











