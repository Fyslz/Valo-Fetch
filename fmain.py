import requests, os, json, time

api_link = "https://valorant-api.com/v1/agents" # save link as string
response = requests.get(api_link) # send request

if response.status_code == 200: # make sure response is 200
    print(f"API Connection succeded, Code: {response.status_code}")
    api_data = response.json() # convert api content to dict\
    agents_data = api_data["data"]
    agent = {}
    valorant_agents = []
    for v in range(len(agents_data)):
        valorant_agents.append(agents_data[v]["displayName"])
        agent[valorant_agents[v]] = {}

    keys_to_check = ["displayIcon", "displayIconSmall", "bustPortrait",
                      "fullPortrait",  "fullPortraitV2", "killfeedPortrait",
                        "minimapPortrait", "background", "role", "abilities"]
    abilities = ["Ability1", "Ability2", "Grenade", "Ultimate", "Passive"]



    for i in range(len(agents_data)):
        for j in range(len(keys_to_check)):
            if keys_to_check[j] == "role":
                # print(keys_to_check[i])
                agent[valorant_agents[i]][f"role_icon"] = agents_data[i][keys_to_check[j]]["displayIcon"]
                
            elif keys_to_check[j] == "abilities":
                for k in range(len(agents_data[i][keys_to_check[j]])):
                    ability_slot = agents_data[i]["abilities"][k]["slot"]
                    ability_name = agents_data[i]["abilities"][k]["displayName"]
                    key = f"{ability_slot}_{ability_name}"
                    value = agents_data[i]["abilities"][k]["displayIcon"]
                    agent[valorant_agents[i]][key] = value

            else:
                key = keys_to_check[j]
                value = agents_data[i][key]
                agent[valorant_agents[i]][key] = value

    base_path = r"C:\Users\na3cl\OneDrive\Documents\valo_fetch"
    os.makedirs(base_path, exist_ok=True)
    for g in range(len(valorant_agents)):
        temp = valorant_agents[g].replace('/', '_')
        agent_folder_path = os.path.join(base_path, temp)
        os.makedirs(agent_folder_path, exist_ok=True)
    print("[=] Finished creating folders")

    
    for m in range(len(valorant_agents)):
        for n in range(len(agent[valorant_agents[m]])):
            data_pairs = agent[valorant_agents[m]]
            buffer = list(data_pairs.items())
            file_name = f"{buffer[n][0].replace('/', '_')}.png"
            image_url = buffer[n][1]
            if image_url == None:
                continue
            print(file_name)
            print(image_url)
            image_path = os.path.join(base_path, valorant_agents[m].replace('/', '_'), file_name)

            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                print(f"[+] Donwloading {valorant_agents[m]}'s : {file_name}")
                with open(image_path, "wb") as file:
                    file.write(img_response.content)
            else:
                print(f"Download Failure, error code: {response.status_code()}")

            time.sleep(0.12)


else:
    print(f"API Connection Failed, Code: {response.status_code}")
