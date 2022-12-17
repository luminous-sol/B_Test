from django.test import TestCase, Client   
from bs4 import BeautifulSoup
from .models import Post


class TestView(TestCase) :
    def test_post_list(self):
        self.client -= Client()
        # client = 컴퓨터
        # 컴퓨터에서 테스트해서 날리면 goorm 에서 돌아간다. 
        
    def test_post_list(self) : #test_test 할 항목
        
        # 1.1 포스트 목록 페이지 가져오는지 확인
        response = self.client.get('/blog/')
        # /blog 해서 urls.py 가서 페이지 가져오는 행동이 잘 되고 있는지 확인하는 것 
        
        # 1.2 정상적으로 페이지가 로드되는지 확인
        self.assertEqual(response.status_code, 200)
        # response의 상태코드가 200과 같은가?
        # 코드 200은 성공 코드로 제대로 load 됐다는 뜻
        
        # 1.3 포스트 목록 페이지의 <title> 태그 중 'Blof'가 있는지 확인
        soup = BeautifulSoup(response.content, 'html.parser')
        # 현재 들어온 내용을 나눠서 html로 바꿔서 저장해줘라
        self.assertEqual(soup.title.text, 'Blog')

        # title 의 text가 Blog와 같은가?
        
        # 1.4 <Nav> Navbar 가 있는지 확인
        navbar = soup.nav 
        # soup 에 nav가 있나? 결과는 navbar에 들어감 
        
        # 1.5 Blog, AboutMe라는 문구가 네비게이션 바에 있는가
        self.assertIn('Blog', navbar.text)
        # assertIn() : 안에 있나?
        # Blog 라는 글자가 navbar안에 있나?
        self.assertIn('About Me', navbar.text)
        # About Me 라는 글자가 navbar 안에 있나?
        
        #--------------------------------------
        
        # 2.1 포스트가 하나도 없는지?
        # test.py는 가상의 DB이기 때문에 영향을 미치지 않는다. 
        self.assertEqual(Post.objects.count(), 0)
        # objects를 셌을 때 0과 같으면 하나도 없다는 뜻
        
        # 2.2 main-area에 '아직 게시물이 없습니다.'라는 문구가 나타난다. 
        main_area = soup.find('div', id="main-area")
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        
        #--------------------------------------
        
        # 3.1 포스트가 2개 있다면 (테스트를 위해 2개를 강제로 만들기)
        post_001 = Post.objects.create(
            title = '첫 번째 포스트 입니다.',
            content = 'Hello World. We are the world',
        )
        
        post_002 = Post.objects.create(
            title = '두 번째 포스트 입니다.',
            content = 'Im the one one and only one.',
        )
        self.assertEqual(Post.objects.count(),2)
        
        # 3.2 포스트 목록 페이지를 새로고침 했을 때
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser') 
        # 파싱이란 구문을 해석할 수 있는 단위로 분할하고 분석하는 과정을 의미한다.
        # 파서는 파싱을 해주는 프로그램을 의미
        self.assertEqual(response.status_code, 200)
        
        #3.3 main-area 에 포스트가 2개 존재한다. 
        main_area = soup.find('div', id='main-area') #div 에서는 main-main_area # div 는 콘텐츠 분할요소로 아무 역할도 하지 않음
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 3.4 '아직 게시물이 없습니다.'라는 문구가 더 이상 나타나지 않는다. 
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)