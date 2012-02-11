#!/usr/bin/python
#
#Copyright (c) 2012 Vinogradov Sergey
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated #documentation files (the "Software"), to deal in the Software without restriction, including without limitation the #rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit #persons to whom the Software is furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the #Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE #WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR #COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR #OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
 The goal of this script is to reduce git commands redundancy.
 Git requirement to write a full command might be a little annoying,
 so this script allows you to write just a few first letters of a Git command.
 For example:
   $ gt st   
 which will mean: git status.
 It's not an analog of Git aliases, it's just a commands shortener.
"""

import sys
import subprocess

# git executable, you should specify
# an absolute path to git program if it's
# not in your PATH variable
_GIT_EXECUTABLE = ['git']

# The most commonly usable Git commands, you can extend it with your favourite commands
_GIT_COMMANDS = frozenset( ['add','archive',
                                        'bisect','branch','blame','bundle',
                                        'checkout','cherry-pick','citool','clone','commit','config',
                                        'diff','describe',
                                        'fetch',
                                        'grep',
                                        'init',
                                        'log',
                                        'merge','mv',
                                        'pull','push',
                                        'rebase','reset','rm',
                                        'show','status','submodule',
                                        'tag'])

def RequestUserInput(suitable_git_commands):
        """ Prints git commands and asks user to input 
            either number of git command or 
            full command to resolve ambiguity
            
            Returns: 
                user inputed data
        """
        print "What did you mean?\n"
        for i, command in enumerate(suitable_git_commands):
            print "" + str( i+1 ) + ") " + command
        print "Enter (number or full command name): "
        return raw_input()
        
def ResolveAmbiguity(suitable_git_commands, ask_user):
    """
        Tries to find an apropriate git command in 
        case of ambiguity.
        
        Params:
            suitable_git_commands - possible commands
            ask_user - function that asks user to specify command
        
    """
    userinput = ask_user(suitable_git_commands)
    selected_command=''
    #TODO: Error handling
    if(userinput.isdigit()):
        index = int(userinput)
        if(index > 0 and index <= len(suitable_git_commands)):
            selected_command = suitable_git_commands[index-1]
    else:
        if userinput in suitable_git_commands:
            selected_command = userinput
    return  selected_command

def SuggestCommand(suitable_git_commands):
    """
        Decides which command in suitable_git_commands is more appropriate
    """
    length = len(suitable_git_commands)
    if length == 1:
        return suitable_git_commands[0]
    if length > 1:
        return ResolveAmbiguity(suitable_git_commands, RequestUserInput)
    return ''

def StartsWithLikeness( gitcommand, command ):
    return gitcommand.startswith(command)

def GenerateSuitableGitCommands(command, likeness_function):
    """ 
        Based on likeness_function result generates a list of Git commands
        which is similar to command param
    """
    return [ gitcommand  for gitcommand in _GIT_COMMANDS if likeness_function(gitcommand, command)]

def TransformParams(params):
    # Function expects that the first param is a Git command.
    #
    # e.g: in 'gt com -m "Initial commit" ' - 'com' comes first.
    #
    # After that, reduced command is replaced by suggested command.
    # In previous example 'com' is replaced by 'commit',
    # if appropriate command is not found, params are returned
    # without any modifications
    command = params[0]
    suitable_commands = GenerateSuitableGitCommands(command, StartsWithLikeness)
    suggested_command = SuggestCommand(suitable_commands)
    if len(suggested_command):
        params[0] = suggested_command
    return params

def GenerateShellCommand(params):
    git_executable = _GIT_EXECUTABLE
    if(len(params)):
        params = TransformParams(params)
    return git_executable+params
    
if __name__=="__main__":
    try:
        shell_command = GenerateShellCommand(sys.argv[1:])
        subprocess.Popen(shell_command,shell=False)
    except OSError, e:
        print >>os.stderr, "Git execution failed ", e
    except KeyboardInterrupt, e:
        pass
