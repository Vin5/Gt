import unittest
import gt

def GenerateAskUserMockFunction(result):
    #generates mock function that returns result
    def ask_user(suitable_git_commands):
        return result
    return ask_user

    
class TestGtFunctions(unittest.TestCase):
    
    # test data for test_GenerateShellCommand
    _CONTROL_COMMAND_STRINGS = [
        'reset',
        'tag start',
        'checkout -b branch1',
        'commit -m "Initial commit"'
    ]
    _TEST_COMMAND_STRINGS = [
        'res',
        't start',
        'chec -b branch1',
        'com -m "Initial commit"'
    ]
    
    # test data for test_ResolveAmbiguity
    _GIT_SUITABLE_COMMANDS = [
        'checkout','cherry-pick','citool','clone','commit','config',
    ]
    
    def test_GenerateShellCommand(self):
        testSequance = zip(self._TEST_COMMAND_STRINGS,self._CONTROL_COMMAND_STRINGS,)
        # test generated shell command and control shell command
        for test_command, control_command in testSequance:
            self.assertEqual(gt.GenerateShellCommand(test_command.split()),'git '+control_command)
        
        self.assertEqual(gt.GenerateShellCommand([]),'git')
        self.assertEqual(gt.GenerateShellCommand(['--version']),'git --version')

    def test_ResolveAmbiguity(self):
        self.assertEqual(
                        gt.ResolveAmbiguity(self._GIT_SUITABLE_COMMANDS,GenerateAskUserMockFunction('1')),
                        'checkout')
        self.assertEqual(
                        gt.ResolveAmbiguity(self._GIT_SUITABLE_COMMANDS,GenerateAskUserMockFunction('6')),
                        'config')
        self.assertEqual(
                        gt.ResolveAmbiguity(self._GIT_SUITABLE_COMMANDS,GenerateAskUserMockFunction('checkout')),
                        'checkout')
        self.assertEqual(
                        gt.ResolveAmbiguity(self._GIT_SUITABLE_COMMANDS,GenerateAskUserMockFunction('-1')),
                        '')
        self.assertEqual(
                        gt.ResolveAmbiguity(self._GIT_SUITABLE_COMMANDS,GenerateAskUserMockFunction('chckt')),
                        '')

if __name__ == '__main__':
    unittest.main()