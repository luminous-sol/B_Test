from django.test import TestCase, Client   
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post, Category


class TestView(TestCase) :
    def setUp(self) :
        self.client = Client()
        # client = 컴퓨터
        # 컴퓨터에서 테스트해서 날리면 goorm 에서 돌아간다. 
        self.user_trump = User.objects.create_user(username='trump'
, password='somepassword')
        self.user_obama = User.objects.create_user(username='obama'
, password='somepassword')
        

    
        self.category_programming = Category.objects.create(name='programming', slug='programming')
        self.category_music = Category.objects.create(name='music', slug='music')

        self.post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello World. We are the world.',
            category=self.category_programming,
            author=self.user_trump
        )

        self.post_002 = Post.objects.create(
            title='두번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            category=self.category_music,
            author=self.user_obama
        )

        self.post_003 = Post.objects.create(
            title='세번째 포스트입니다.',
            content='category가 없을 수도 있죠',
            author=self.user_obama
        )

    
    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text) # navbar text 중에 'Blog'가 있나
        self.assertIn('About Me', navbar.text) # navbar text 중에 'About Me 가 있나'
        
        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'],'/') # 뒤에 아무것도 안 붙는 홈으로 가는 것
        
        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attr['href'], '/') # 뒤에 아무것도 안 붙는 홈으로 가는 것
        
        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attr['href'], '/blog/') # 뒤에 blog/ 붙는 링크
        
        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attr['href'], '/about_me/') # 뒤에 about_me/ 붙는 링크       

    def category_card_test(self, soup):
        categories_card = soup.find('div', id='categories-card')
        self.assertIn('Categories', categories_card.text)
        self.assertIn(
            f'{self.category_programming.name} ({self.category_programming.post_set.count()})',
            categories_card.text
        )
        self.assertIn(
            f'{self.category_music.name} ({self.category_music.post_set.count()})',
            categories_card.text
        )
        self.assertIn(f'미분류 (1)', categories_card.text)
        
    def test_post_list(self) : #test_test 할 항목
        
        
        # Post가 있는 경우
        self.assertEqual(Post.objects.count(), 3)

        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.assertEqual(soup.title.text, 'Blog')

#        self.navbar_test(soup)
        self.category_card_test(soup)

        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        post_001_card = main_area.find('div', id='post-1')  # id가 post-1인 div를 찾아서, 그 안에
        self.assertIn(self.post_001.title, post_001_card.text)  # title이 있는지
        self.assertIn(self.post_001.category.name, post_001_card.text)  # category가 있는지
        self.assertIn(self.post_001.author.username.upper(), post_001_card.text)  # 작성자명이 있는지

        post_002_card = main_area.find('div', id='post-2')
        self.assertIn(self.post_002.title, post_002_card.text)
        self.assertIn(self.post_002.category.name, post_002_card.text)
        self.assertIn(self.post_002.author.username.upper(), post_002_card.text)

        post_003_card = main_area.find('div', id='post-3')
        self.assertIn('미분류', post_003_card.text)
        self.assertIn(self.post_003.title, post_003_card.text)
        self.assertIn(self.post_003.author.username.upper(), post_003_card.text)

        # Post가 없는 경우
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        main_area = soup.find('div', id='main-area')  # id가 main-area인 div태그를 찾습니다.
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        # # 1.1 포스트 목록 페이지 가져오는지 확인
        # response = self.client.get('/blog/')
        # # /blog 해서 urls.py 가서 페이지 가져오는 행동이 잘 되고 있는지 확인하는 것 
        
        # # 1.2 정상적으로 페이지가 로드되는지 확인
        # self.assertEqual(response.status_code, 200)
        # # response의 상태코드가 200과 같은가?
        # # 코드 200은 성공 코드로 제대로 load 됐다는 뜻
        
        # # 1.3 포스트 목록 페이지의 <title> 태그 중 'Blof'가 있는지 확인
        # soup = BeautifulSoup(response.content, 'html.parser')
        # # 현재 들어온 내용을 나눠서 html로 바꿔서 저장해줘라
        # self.assertEqual(soup.title.text, 'Blog')

        # # title 의 text가 Blog와 같은가?
        
        # # 1.4 <Nav> Navbar 가 있는지 확인
        # # navbar = soup.nav 
        # # # soup 에 nav가 있나? 결과는 navbar에 들어감 
        
        # # # 1.5 Blog, AboutMe라는 문구가 네비게이션 바에 있는가
        # # self.assertIn('Blog', navbar.text)
        # # # assertIn() : 안에 있나?
        # # # Blog 라는 글자가 navbar안에 있나?
        # # self.assertIn('About Me', navbar.text)
        # # # About Me 라는 글자가 navbar 안에 있나?
        
        # #--------------------------------------
        
        # # 2.1 포스트가 하나도 없는지?
        # # test.py는 가상의 DB이기 때문에 영향을 미치지 않는다. 
        # self.assertEqual(Post.objects.count(), 0)
        # # objects를 셌을 때 0과 같으면 하나도 없다는 뜻
        
        # # 2.2 main-area에 '아직 게시물이 없습니다.'라는 문구가 나타난다. 
        # main_area = soup.find('div', id="main-area")
        # self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        # #--------------------------------------
        
        # # 3.1 포스트가 2개 있다면 (테스트를 위해 2개를 강제로 만들기)
        # post_001 = Post.objects.create(
        #     title = '첫 번째 포스트 입니다.',
        #     content = 'Hello World. We are the world',
        #     author = self.user_trump
        # )
        
        # post_002 = Post.objects.create(
        #     title = '두 번째 포스트 입니다.',
        #     content = 'Im the one one and only one.',
        #     author = self.user_obama,
        # )
        

        
#         self.assertEqual(Post.objects.count(),2)
        
#         # 3.2 포스트 목록 페이지를 새로고침 했을 때
#         response = self.client.get('/blog/')
#         soup = BeautifulSoup(response.content, 'html.parser') 
#         # 파싱이란 구문을 해석할 수 있는 단위로 분할하고 분석하는 과정을 의미한다.
#         # 파서는 파싱을 해주는 프로그램을 의미
#         self.assertEqual(response.status_code, 200)
        
#         #3.3 main-area 에 포스트가 2개 존재한다. 
#         main_area = soup.find('div', id='main-area') #div 에서는 main-main_area # div 는 콘텐츠 분할요소로 아무 역할도 하지 않음
#         self.assertIn(post_001.title, main_area.text)
#         self.assertIn(post_002.title, main_area.text)

#         self.assertIn(self.user_trump.username.upper(), main_area.text)
#         self.assertIn(self.user_obama.username.upper(), main_area.text)        
        
#         # 3.4 '아직 게시물이 없습니다.'라는 문구가 더 이상 나타나지 않는다. 
#         self.assertNotIn('아직 게시물이 없습니다', main_area.text)
    
    
#     #--------------------------------------
    
    def test_post_detail(self): # 매개변수로 받는 게 없더라도 self 적어야 한다 # pk도 같이 받는다면 self, pk 
        self.assertEqual(self.post_001.get_absolute_url(), '/blog/1/')

        response = self.client.get(self.post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        self.assertIn(self.post_001.title, soup.title.text)

        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(self.post_001.title, post_area.text)
        self.assertIn(self.category_programming.name, post_area.text)

        self.assertIn(self.user_trump.username.upper(), post_area.text)
        self.assertIn(self.post_001.content, post_area.text)

        # # 1.1 포스트 하나 생성하기
        # post_001 = Post.objects.create(
        #     title = '첫 번째 포스트 입니다.',
        #     content = 'Hello World. We are the world',
        #     author = self.user_trump
        # )
        
        # # 1.2 포스트 url은 (상세 페이지 주소) '/blog/1/' 이렇게 pk가 붙어있다. 
        # # 지금은 포스트 하나니까 1 넣어서 검사
        # self.assertEqual(post_001.get_absolute_url(), '/blog/1/') 
        # # get_absolute_url 는 reverse함수를 통해 모델 개별 데이터 url을 문자열로 반환
        
        # #--------------------------------------
    
        # # 2. 첫 번째 포스트의 상세 페이지 검사하기
        # # 2.1 첫 번째 포스트의 url로 접근하면 정상적으로 작동하는가
        # response = self.client.get(post_001.get_absolute_url())
        # # 1.2 에서 검증한 blog/1을 가져온다. 
        # soup = BeautifulSoup(response.content, 'html.parser') # response 안의 content , html 파일을 파싱
        # self.assertEqual(response.status_code, 200)
        
        # # 2.2 포스트의 목록 페이지와 같은 navbar가 붙어있는가?
        # navbar = soup.nav 
        # self.assertIn('Blog', navbar.text)
        # self.assertIn('About Me', navbar.text)
        
        # # 2.3 첫 번째 포스트의 제목이 웹 브라우저 탭 타이틀에 들어잇는가?
        # self.assertIn(post_001.title, soup.title.text)
        
        # # 2.4 첫 번째 포스트의 제목이 포스트 영역에 있는가?
        # main_area = soup.find('div', id ='main-area')
        # post_area = main_area.find('div', id='post-area')
        # self.assertIn(post_001.title, post_area.text)
        
        # # 2.5 첫 번째 포스트의 작성자가 포스트 영역에 있는가(지금은 아직 구현 X)
        
        # # 2.6 첫 번째 포스트의 내용이 포스트 영역에 있는가
        # self.assertIn(post_001.content, post_area.text)
        # # html parser 했으니까 text 로 적어주는 것 
        
        # self.assertIn(self.user_trump.username.upper(), post_area.text)
        # #--------------------------------------
        
    def test_category_page(self):
        response = self.client.get(self.category_programming.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        self.navbar_test(soup)
        self.category_card_test(soup)

        

        main_area = soup.find('div', id='main-area')
        self.assertIn(self.category_programming.name, main_area.text)
        self.assertIn(self.post_001.title, main_area.text)
        self.assertNotIn(self.post_002.title, main_area.text)
        self.assertNotIn(self.post_003.title, main_area.text)

    #--------------------------------------
    
