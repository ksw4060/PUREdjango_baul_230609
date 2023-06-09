from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model #사용자가 있는지 검사하는 함수
from django.contrib import auth
from django.shortcuts import render, redirect
from user.models import UserModel
from django.contrib import messages



def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated  # 로그인 된 사용자가 요청하는지 검사
        if user:  # 로그인이 되어있다면
            return redirect('/')
        else:  # 로그인이 되어있지 않다면
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        email = request.POST.get('email', '')
        account = request.POST.get('account', '')
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        introduction = request.POST.get('introduction', '')

        if password != password2:
            # 패스워드가 다르다는 에러가 필요합니다. {'error':'에러문구'} 를 만들어서 전달합니다.
            return render(request, 'user/signup.html', {'error': '패스워드를 확인 해 주세요!'})
        else:
            if username == '' or password == '' or account =='' or email =='':
                # account과 username과 password과 email가 필수
                return render(request, 'user/signup.html', {'error': '사용자 이름과 계정과 패스워드와 이메일은 필수 값 입니다'})

            exist_user = get_user_model().objects.filter(account=account)
            if exist_user:
                return render(request, 'user/signup.html', {'error':'사용자가 존재합니다.'})  # 사용자가 존재하기 때문에 사용자를 저장하지 않고 회원가입 페이지를 다시 띄움
            else:
                UserModel.objects.create_user(email=email, account=account, username=username, password=password, introduction=introduction)
                return redirect('sign-in')  # 회원가입이 완료되었으므로 로그인 페이지로 이동
# 회원 가입시, 이미 존재하는 유저이다 > 회원 가입 할 필요 없음
# 이미 존하는 유저가 아니다 > 회원 가입 시켜야함


def sign_in_view(request):
    if request.method == 'POST':
        account = request.POST.get('account', '')
        password = request.POST.get('password', '')

        me = auth.authenticate(request, account=account, password=password)  # 사용자 불러오기
        if me is not None:  # 저장된 사용자의 패스워드와 입력받은 패스워드 비교
            auth.login(request, me)
            return redirect('home')
        else:
            return render(request, 'user/signin.html', {'error' : '계정이 없거나 패스워드가 잘못입력되었습니다'})  # 로그인 실패
    elif request.method == 'GET':
        user = request.user.is_authenticated  # 사용자가 로그인 되어 있는지 검사
        if user:  # 로그인이 되어 있다면
            return redirect('home')
        else:  # 로그인이 되어 있지 않다면
            return render(request, 'user/signin.html')



@login_required
def logout(request):
    auth.logout(request) # 인증 되어있는 정보를 없애기
    return redirect('home')


@login_required
def user_view(request):
    if request.method == 'GET':
        # 사용자를 불러오기, exclude와 request.user.username 를 사용해서 '로그인 한 사용자'를 제외하기
        user_list = UserModel.objects.all().exclude(username=request.user.username)
        return render(request, 'user/user_list.html', {'user_list': user_list})


@login_required
def user_follow(request, id):
    me = request.user
    click_user = UserModel.objects.get(id=id)
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('user-list')
