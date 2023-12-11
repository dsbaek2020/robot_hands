from random import randint

print(
   '''
   Hello This is the Rock paper Scissors Game.
   
   플레이방법: 가위<바위, 바위<보 보<가위. 이 3게중 하나를 골라 승패 혹은 무승부를 가리는 게임
   
   *무승부가나오는 경우는 서로 낸게 같을 경우
   
   *무승부가 나올시 다시한다
   
   ''' )


rule = {'r-r': '무승부',
         's-s': '무승부',
         'p-p': '무승부',

         'r-p': '졌습니다.',
         'r-s': '승리했습니다.',

         's-p': '승리했습니다.',
         's-r': '졌습니다.',

         'p-r': '승리했습니다.',
         'p-s' : '졌습니다.'
}


print('시작합니다.')

#
rps = ['r', 'p', 's']

#
yourChoice = input('가위(s) 바위(r) 보(p) 중에 하나 골라봐')


# cpu의 가위바위보 선택값을 정하기 위해서, 난수를 0~2사이로 생성하고
# 그 난수를 [] 연산자 안에 넣어 rps 리스트의 항목 하나를 읽어 온다.
# 읽어온 값은  cpuChoice 변수에  저장한다.
cpuChoice = rps[ randint(0,2) ]

print('너는 {}뽑았으며, 나(CPU)는 {}냈다.'.format(yourChoice, cpuChoice) )


#print rule에 yourChoice+ - +cpuCoice를 하면 rule에서 y-c값에 s키를 가지고온다 그후 그값을 프린트하는 것이다
print(rule[yourChoice+'-'+cpuChoice])
