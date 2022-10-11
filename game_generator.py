#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  3 16:25:28 2022

@author: Hassan061
"""
#%%
import re
import openai
from time import time,sleep
from uuid import uuid4
import random



def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()
    
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

#Get your openai API key from https://beta.openai.com/account/api-keys

openai.api_key = open_file('openaiapi.txt')
#%%

top_level_genres = open_file("./Game_Elements/TopLevelGenres.txt")
genres = open_file("./Game_Elements/Genres.txt")
sub_genres = open_file("./Game_Elements/SubGenres.txt")
visuals = open_file("./Game_Elements/VisualsViewPoints.txt")
theme = open_file("./Game_Elements/ThemesMoods.txt")
features = open_file("./Game_Elements/Features.txt")
players = open_file("./Game_Elements/Players.txt")
assessment = open_file("./Game_Elements/Assessment.txt")


#%%
def gpt3_completion(prompt,top_level_genres, genres, theme1, theme2, engine='text-davinci-002', temp=1, top_p=1, tokens=3500, freq_pen=0.5, pres_pen=0.0, stop=['asdfasdf', 'asdasdf']):
    
    
    max_retry = 5
    retry = 0
    prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()  # force it to fix any unicode errors
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            
            text = text.replace('GAME OVERVIEW: ','\n\nGAME OVERVIEW: ') \
            .replace('GAME OBJECTIVES: ', '\n\nGAME OBJECTIVES: ').replace("GAME RULES: ",'\n\nGAME RULES: ') \
            .replace("MAIN GAME LOOP: ", "\n\nMAIN GAME LOOP: ") \
            .replace("GAME LOOP: ", "\n\nGAME LOOP: ") \
            .replace("GAME ENVIRONMENT: ","\n\nGAME ENVIRONMENT: ") \
            .replace("CHARACTERS: ", "\n\nCHARACTERS: ") \
            .replace("UNIQUE SELLING POINTS:", "\n\nUNIQUE SELLING POINTS: ")
            
            ud = str(time()).split('.')[1]
            filename = f'{top_level_genres}_{genres}_{theme1}_{theme2}_{ud}.txt' 
            filename = filename.replace(" ", '$')
            
            a = prompt.split('\n\n\n')
            
            print(filename)
            
            # Where the GDD's would be saved
            elements = a[0].split("\n\n")[1]
            
            save_file('Generated_GDD/%s' % filename, elements + '\n\n==========\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)
            
#%%
def pick_random(filename):
    lines = open_file(filename).splitlines()
    return random.choice(lines)

#%%
def pick_random2(filename):
    lines = open_file(filename).splitlines()
    r = random.sample(lines, 2)
    
    return r[0], r[1]


#%%
def generate_synopsis():
   
    # Pick a random element from each category
    
    top_level_genres = pick_random("./Game_Elements/TopLevelGenres.txt")
    genres = pick_random("./Game_Elements/Genres.txt")
    sub_genres = pick_random("./Game_Elements/SubGenres.txt")
    visuals = pick_random("./Game_Elements/VisualsViewPoints.txt")
    theme1, theme2 = pick_random2("./Game_Elements/ThemesMoods.txt")
    features = pick_random("./Game_Elements/Features.txt")
    #Team-Based
    
    if (genres == 'MMORPG') | (genres == 'MOBA') | (genres == 'Party-Based RPG') | (features == 'Team-Based'):
        players = "Multiplayer"
    else:
        players = pick_random("./Game_Elements/Players.txt")
        
    assessment = pick_random("./Game_Elements/Assessment.txt")
    
    
    
    

    
    
    prompt = open_file('prompt_synopsis.txt')
    
    prompt = prompt.replace('<<TOP LEVEL GENRE>>', top_level_genres)
    prompt = prompt.replace('<<GENRE>>', genres)
    prompt = prompt.replace('<<SUB GENRE>>', sub_genres)
    prompt = prompt.replace('<<VISUALS>>', visuals)
    prompt = prompt.replace('<<THEME1>>', theme1)
    prompt = prompt.replace('<<THEME2>>', theme2)
    prompt = prompt.replace('<<FEATURES>>', features)
    prompt = prompt.replace('<<PLAYERS>>', players)
    prompt = prompt.replace('<<ASSESSMENT>>', assessment)
    prompt = prompt.replace('<<UUID>>', str(uuid4()))
    
    print('\n\nTop level genre:', top_level_genres)
    print('Genre:', genres)
    print('Sub Genre:', sub_genres)
    print('Visuals:', visuals)
    print('Theme 1:', theme1)
    print('Theme 2:', theme2)
    print('Features:', features)
    print('Players:', players)
    print('Assessment:', assessment)
    
    
        
    
    # generate and save synopsis
   
    gpt3_completion(prompt,top_level_genres, genres, theme1, theme2)

#%%

if __name__ == '__main__':
    random.seed()
    for i in list(range(0,5)): #how many prompts to generate
        generate_synopsis()
      