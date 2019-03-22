from django.test import TestCase
from django.test import Client
import json
from movie.models import Movie, Comment


class MoviePOSTTestcase(TestCase):
    def setUp(self):
        self.c = Client()
        self.lock = {"id":1, "Title":"Lock","Year":"2016","Rated":"N/A","Released":"14 Oct 2016","Runtime":"92 min","Genre":"Thriller","Director":"Smeep Kang","Writer":"Pali Bhupinder Singh (dialogue), Pali Bhupinder Singh (screenplay)","Actors":"Gippy Grewal, Smeep Kang, Geeta Basra, Gurpreet Ghuggi","Plot":"A screenwriter loses a script in the back of a rickshaw, and complications in the driver's life make it difficult to return to its rightful owner.","Language":"Punjabi","Country":"India","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BYTJmZGFlYTgtNWRmZi00NmQ0LWJmMTQtMWZjNWViZmY3NGI4XkEyXkFqcGdeQXVyNjQ1MTMyMzQ@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '6.2/10'}]","Metascore":"N/A","imdbRating":"6.2","imdbVotes":"105","imdbID":"tt6103292","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","TotalSeasons":""}
        self.snatch = {"id":2,"Title":"Snatch","Year":"2000","Rated":"R","Released":"19 Jan 2001","Runtime":"102 min","Genre":"Comedy, Crime","Director":"Guy Ritchie","Writer":"Guy Ritchie","Actors":"Benicio Del Toro, Dennis Farina, Vinnie Jones, Brad Pitt","Plot":"Unscrupulous boxing promoters, violent bookmakers, a Russian gangster, incompetent amateur robbers and supposedly Jewish jewelers fight to track down a priceless stolen diamond.","Language":"English, Russian","Country":"UK, USA","Awards":"4 wins & 6 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BMTA2NDYxOGYtYjU1Mi00Y2QzLTgxMTQtMWI1MGI0ZGQ5MmU4XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '8.3/10'}, {'Source': 'Rotten Tomatoes', 'Value': '73%'}, {'Source': 'Metacritic', 'Value': '55/100'}]","Metascore":"55","imdbRating":"8.3","imdbVotes":"708,496","imdbID":"tt0208092","Type":"movie","DVD":"03 Jul 2001","BoxOffice":"$30,093,107","Production":"Columbia Pictures","Website":"N/A","TotalSeasons":""}
        self.lord = {"id":3,"Title":"The Lord of the Rings: The Fellowship of the Ring","Year":"2001","Rated":"PG-13","Released":"19 Dec 2001","Runtime":"178 min","Genre":"Adventure, Drama, Fantasy","Director":"Peter Jackson","Writer":"J.R.R. Tolkien (novel), Fran Walsh (screenplay), Philippa Boyens (screenplay), Peter Jackson (screenplay)","Actors":"Alan Howard, Noel Appleby, Sean Astin, Sala Baker","Plot":"A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.","Language":"English, Sindarin","Country":"New Zealand, USA","Awards":"Won 4 Oscars. Another 113 wins & 123 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '8.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '91%'}, {'Source': 'Metacritic', 'Value': '92/100'}]","Metascore":"92","imdbRating":"8.8","imdbVotes":"1,484,789","imdbID":"tt0120737","Type":"movie","DVD":"06 Aug 2002","BoxOffice":"$314,000,000","Production":"New Line Cinema","Website":"http://www.lordoftherings.net/film/trilogy/thefellowship.html","TotalSeasons":""}
    def test_title_not_given(self):
        test_data = {"response": False, "error": "search title is missing"}
        response = self.c.post('/movies/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data, response_dict)

    def test_title_not_found_in_OMDb(self):
        test_data = {"response": False, "error": "title is not found in OMDb"}

        response = self.c.post('/movies/qwertyuiop/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data, response_dict)

    def test_datafrom_OMDb_save_to_local_db(self):
        omdb_data = {"id":1,"Title":"Lock","Year":"2016","Rated":"N/A","Released":"14 Oct 2016","Runtime":"92 min","Genre":"Thriller","Director":"Smeep Kang","Writer":"Pali Bhupinder Singh (dialogue), Pali Bhupinder Singh (screenplay)","Actors":"Gippy Grewal, Smeep Kang, Geeta Basra, Gurpreet Ghuggi","Plot":"A screenwriter loses a script in the back of a rickshaw, and complications in the driver's life make it difficult to return to its rightful owner.","Language":"Punjabi","Country":"India","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BYTJmZGFlYTgtNWRmZi00NmQ0LWJmMTQtMWZjNWViZmY3NGI4XkEyXkFqcGdeQXVyNjQ1MTMyMzQ@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '6.2/10'}]","Metascore":"N/A","imdbRating":"6.2","imdbVotes":"105","imdbID":"tt6103292","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","TotalSeasons":""}


        response = self.c.post('/movies/lock/')
        db_record = Movie.objects.filter(imdbID='tt6103292').values()[0]
        self.assertDictEqual(omdb_data, db_record)

    def test_add_movie(self):
        test_data0 = {"response": True, "result":[self.lock]}
        test_data1 = {"response": True, "result":[self.lock, self.snatch]}
        test_data2 = {"response": True, "result":[self.lock, self.snatch, self.lord]}


        self.c.post('/movies/lock/')
        response = self.c.get('/movies/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data0, response_dict)

        self.c.post('/movies/snatch/')
        response = self.c.get('/movies/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data1, response_dict)

        self.c.post('/movies/lord/')
        response = self.c.get('/movies/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data2, response_dict)


class MovieGETTestcase(TestCase):
    def setUp(self):
        self.c = Client()
        self.lock = {"id":1, "Title":"Lock","Year":"2016","Rated":"N/A","Released":"14 Oct 2016","Runtime":"92 min","Genre":"Thriller","Director":"Smeep Kang","Writer":"Pali Bhupinder Singh (dialogue), Pali Bhupinder Singh (screenplay)","Actors":"Gippy Grewal, Smeep Kang, Geeta Basra, Gurpreet Ghuggi","Plot":"A screenwriter loses a script in the back of a rickshaw, and complications in the driver's life make it difficult to return to its rightful owner.","Language":"Punjabi","Country":"India","Awards":"N/A","Poster":"https://m.media-amazon.com/images/M/MV5BYTJmZGFlYTgtNWRmZi00NmQ0LWJmMTQtMWZjNWViZmY3NGI4XkEyXkFqcGdeQXVyNjQ1MTMyMzQ@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '6.2/10'}]","Metascore":"N/A","imdbRating":"6.2","imdbVotes":"105","imdbID":"tt6103292","Type":"movie","DVD":"N/A","BoxOffice":"N/A","Production":"N/A","Website":"N/A","TotalSeasons":""}
        self.snatch = {"id":2,"Title":"Snatch","Year":"2000","Rated":"R","Released":"19 Jan 2001","Runtime":"102 min","Genre":"Comedy, Crime","Director":"Guy Ritchie","Writer":"Guy Ritchie","Actors":"Benicio Del Toro, Dennis Farina, Vinnie Jones, Brad Pitt","Plot":"Unscrupulous boxing promoters, violent bookmakers, a Russian gangster, incompetent amateur robbers and supposedly Jewish jewelers fight to track down a priceless stolen diamond.","Language":"English, Russian","Country":"UK, USA","Awards":"4 wins & 6 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BMTA2NDYxOGYtYjU1Mi00Y2QzLTgxMTQtMWI1MGI0ZGQ5MmU4XkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '8.3/10'}, {'Source': 'Rotten Tomatoes', 'Value': '73%'}, {'Source': 'Metacritic', 'Value': '55/100'}]","Metascore":"55","imdbRating":"8.3","imdbVotes":"708,496","imdbID":"tt0208092","Type":"movie","DVD":"03 Jul 2001","BoxOffice":"$30,093,107","Production":"Columbia Pictures","Website":"N/A","TotalSeasons":""}
        self.lord = {"id":3,"Title":"The Lord of the Rings: The Fellowship of the Ring","Year":"2001","Rated":"PG-13","Released":"19 Dec 2001","Runtime":"178 min","Genre":"Adventure, Drama, Fantasy","Director":"Peter Jackson","Writer":"J.R.R. Tolkien (novel), Fran Walsh (screenplay), Philippa Boyens (screenplay), Peter Jackson (screenplay)","Actors":"Alan Howard, Noel Appleby, Sean Astin, Sala Baker","Plot":"A meek Hobbit from the Shire and eight companions set out on a journey to destroy the powerful One Ring and save Middle-earth from the Dark Lord Sauron.","Language":"English, Sindarin","Country":"New Zealand, USA","Awards":"Won 4 Oscars. Another 113 wins & 123 nominations.","Poster":"https://m.media-amazon.com/images/M/MV5BN2EyZjM3NzUtNWUzMi00MTgxLWI0NTctMzY4M2VlOTdjZWRiXkEyXkFqcGdeQXVyNDUzOTQ5MjY@._V1_SX300.jpg","Ratings":"[{'Source': 'Internet Movie Database', 'Value': '8.8/10'}, {'Source': 'Rotten Tomatoes', 'Value': '91%'}, {'Source': 'Metacritic', 'Value': '92/100'}]","Metascore":"92","imdbRating":"8.8","imdbVotes":"1,484,789","imdbID":"tt0120737","Type":"movie","DVD":"06 Aug 2002","BoxOffice":"$314,000,000","Production":"New Line Cinema","Website":"http://www.lordoftherings.net/film/trilogy/thefellowship.html","TotalSeasons":""}
    def test_no_sort_column_given(self):
        self.maxDiff = None
        test_data = {"response": True, "result":[self.lock, self.snatch, self.lord]}


        self.c.post('/movies/lock/')
        self.c.post('/movies/snatch/')
        self.c.post('/movies/lord/')
        response = self.c.get('/movies/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data, response_dict)

    def test_sort_by_column(self):
        self.maxDiff = None
        test_data0 = {"response": True, "result":[self.lord, self.snatch, self.lock]}
        test_data1 = {"response": True, "result":[self.snatch, self.lord, self.lock]}



        self.c.post('/movies/lock/')
        self.c.post('/movies/snatch/')
        self.c.post('/movies/lord/')
        response = self.c.get('/movies/imdbID/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data0, response_dict)


        response = self.c.get('/movies/Director/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data1, response_dict)


    def test_sort_by_column_desc(self):
        self.maxDiff = None
        test_data0 = {"response": True, "result":[self.lord, self.snatch, self.lock]}
        test_data1 = {"response": True, "result":[self.lock, self.lord, self.snatch]}


        self.c.post('/movies/lock/')
        self.c.post('/movies/snatch/')
        self.c.post('/movies/lord/')
        response = self.c.get('/movies/Title/DESC')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data0, response_dict)

        response = self.c.get('/movies/Director/DESC')
        response_dict = json.loads(response.content)
        self.assertDictEqual(test_data1, response_dict)

class CommentPOSTTestcase(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.post('/movies/lock/')
        self.c.post('/movies/snatch/')
        self.c.post('/movies/lord/')
        self.test_data0 = {"response":True, "result": {"imdbID": "tt6103292", "comment": "ABC"}}
        self.test_data1 = {"response":False, "error": "imdbID and comment are required"}
        self.test_data2 = {"response":False, "error": "chosen imdbID doesn't exist in movie table"}
        self.test_data3 = {"response": True, "result": [{"imdbID":"tt0208092", "comment":"ABC"}]}
        self.test_data4 = {"response": True, "result": [{"imdbID":"tt0208092", "comment":"ABC"},{"imdbID":"tt0120737", "comment":"DEF"}]}


    def test_add_comment(self):
        self.c.post('/comments/tt0208092/ABC')
        response = self.c.get('/comments/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data3, response_dict)

        self.c.post('/comments/tt0120737/DEF')
        response = self.c.get('/comments/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data4, response_dict)

    def test_no_id(self):
        response = self.c.post('/comments/tt6103292/ABC')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        response = self.c.post('/comments/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data1, response_dict)

    def test_no_comment(self):
        response = self.c.post('/comments/tt6103292/ABC')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        response = self.c.post('/comments/tt6103292/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data1, response_dict)

    def test_id_not_in_db(self):
        response = self.c.post('/comments/tt6103292/ABC')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        response = self.c.post('/comments/tt0123456/DEF')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data2, response_dict)


class CommentGETTestcase(TestCase):
    def setUp(self):
        self.c = Client()
        self.c.post('/movies/lock/')
        self.c.post('/movies/snatch/')
        self.c.post('/movies/lord/')
        self.c.post('/comments/tt6103292/ABC')
        self.c.post('/comments/tt0208092/DEF')
        self.c.post('/comments/tt0120737/GHI')

        self.test_data0 = {"response": True, "result": [{"imdbID": "tt6103292", "comment": "ABC"}]}
        self.test_data1 = {"response": False, "error": "chosen imdbID doesn't exist in comment table"}
        self.test_data2 = {"response": True, "result": [{"imdbID": "tt6103292", "comment": "ABC"},{"imdbID":"tt0208092", "comment":"DEF"},{"imdbID":"tt0120737", "comment":"GHI"}]}
        self.test_data3 =  {"response": True, "result": [{"imdbID": "tt6103292", "comment": "ABC"},{"imdbID":"tt0208092", "comment":"DEF"},{"imdbID":"tt0120737", "comment":"GHI"},{"imdbID": "tt6103292", "comment": "JKL"},{"imdbID":"tt0208092", "comment":"MNO"},{"imdbID":"tt0120737", "comment":"PQR"}]}

    def test_id_not_in_db(self):
        response = self.c.get('/comments/tt6103292/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        response = self.c.get('/comments/tt0123456/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data1, response_dict)

    def test_no_id(self):
        response = self.c.get('/comments/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data2, response_dict)

        self.c.post('/comments/tt6103292/JKL')
        self.c.post('/comments/tt0208092/MNO')
        self.c.post('/comments/tt0120737/PQR')
        response = self.c.get('/comments/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data3, response_dict)

class TopGETTestcase(TestCase):
    def setUp(self):
        self.maxDiff = None
        self.c = Client()
        test_movies = ["lock/","snatch/","lord/","omen/","goodfellas/","departed/","casino/","back+to/","forrest/","raging+bull/","lock+stock/","shining/","full+metal+jacket/","a+clockwork/","karate+kid/","terminator/","heat/","beach/","shaolin+soccer/","a+better+tomorrow/"]
        for i in test_movies:
            self.c.post("/movies/" + i)

        self.test_comments = ["tt6103292","tt0208092","tt0120737","tt0371267","tt0099685","tt6854314","tt0112641","tt0088763","tt0109830","tt0081398","tt0120735","tt0081505","tt0093058","tt0426060","tt0066921","tt5817168","tt0113277","tt0163978","tt0286112","tt0092263"]
        for i in range(12,21):
            for j in range(i):
                self.c.post("/comments/" + self.test_comments[i-1] + "/ABC")


        self.test_data0 = {"response": True, "results": [{"rank":1,"imdbID":"tt0092263","total":20},{"rank":2,"imdbID":"tt0286112","total":19},{"rank":3,"imdbID":"tt0163978","total":18},{"rank":4,"imdbID":"tt0113277","total":17},{"rank":5,"imdbID":"tt5817168","total":16},{"rank":6,"imdbID":"tt0066921","total":15},{"rank":7,"imdbID":"tt0426060","total":14},{"rank":8,"imdbID":"tt0093058","total":13},{"rank":9,"imdbID":"tt0081505","total":12}]}

        self.test_data1 = {"response": True, "results": [{"rank":1,"imdbID":"tt0109830","total":21},{"rank":2,"imdbID":"tt0092263","total":20},{"rank":3,"imdbID":"tt0286112","total":19},{"rank":4,"imdbID":"tt0163978","total":18},{"rank":5,"imdbID":"tt0113277","total":17},{"rank":6,"imdbID":"tt5817168","total":16},{"rank":7,"imdbID":"tt0066921","total":15},{"rank":8,"imdbID":"tt0426060","total":14},{"rank":9,"imdbID":"tt0093058","total":13},{"rank":10,"imdbID":"tt0081505","total":12}]}

        self.test_data2 = {"response": True, "results": [{"rank":1,"imdbID":"tt0109830","total":21},{"rank":2,"imdbID":"tt0092263","total":20},{"rank":3,"imdbID":"tt0286112","total":19},{"rank":4,"imdbID":"tt0163978","total":18},{"rank":5,"imdbID":"tt0113277","total":17},{"rank":6,"imdbID":"tt0088763","total":16},{"rank":6,"imdbID":"tt5817168","total":16},{"rank":7,"imdbID":"tt0066921","total":15},{"rank":8,"imdbID":"tt0426060","total":14},{"rank":9,"imdbID":"tt0093058","total":13},{"rank":10,"imdbID":"tt0081505","total":12}]}

        self.test_data3 = {"response": True, "results": [{"rank":1,"imdbID":"tt0092263","total":20},{"rank":1,"imdbID":"tt0112641","total":20},{"rank":2,"imdbID":"tt0286112","total":19},{"rank":3,"imdbID":"tt0163978","total":18},{"rank":4,"imdbID":"tt0113277","total":17},{"rank":5,"imdbID":"tt5817168","total":16},{"rank":6,"imdbID":"tt0066921","total":15},{"rank":7,"imdbID":"tt0426060","total":14},{"rank":8,"imdbID":"tt0093058","total":13},{"rank":9,"imdbID":"tt0081505","total":12}]}

        self.test_data4 = {"response": True, "results": [{"rank":1,"imdbID":"tt0092263","total":20},{"rank":1,"imdbID":"tt0112641","total":20},{"rank":2,"imdbID":"tt0286112","total":19},{"rank":3,"imdbID":"tt0163978","total":18},{"rank":4,"imdbID":"tt0113277","total":17},{"rank":5,"imdbID":"tt5817168","total":16},{"rank":6,"imdbID":"tt0066921","total":15},{"rank":7,"imdbID":"tt0426060","total":14},{"rank":8,"imdbID":"tt0093058","total":13},{"rank":8,"imdbID":"tt6854314","total":13},{"rank":9,"imdbID":"tt0081505","total":12}]}

        self.test_data5 = {"response": True, "results": [{"rank":1,"imdbID":"tt0092263","total":20},{"rank":1,"imdbID":"tt0112641","total":20},{"rank":2,"imdbID":"tt0286112","total":19},{"rank":3,"imdbID":"tt0163978","total":18},{"rank":4,"imdbID":"tt0113277","total":17},{"rank":5,"imdbID":"tt5817168","total":16},{"rank":6,"imdbID":"tt0066921","total":15},{"rank":7,"imdbID":"tt0426060","total":14},{"rank":8,"imdbID":"tt0093058","total":13},{"rank":8,"imdbID":"tt0099685","total":13},{"rank":8,"imdbID":"tt6854314","total":13},{"rank":9,"imdbID":"tt0081505","total":12}]}

    def test_only_show_top10(self):
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        self.test_data0["results"].append({"rank":10,"imdbID":"tt0120735","total":11})
        for i in range(11):
            self.c.post("/comments/" + self.test_comments[10] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

        for i in range(10):
            self.c.post("/comments/" + self.test_comments[9] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data0, response_dict)

    def test_order_by_rank(self):
        for i in range(21):
            self.c.post("/comments/" + self.test_comments[8] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data1, response_dict)

        for i in range(16):
            self.c.post("/comments/" + self.test_comments[7] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data2, response_dict)

    def test_same_rank(self):
        for i in range(20):
            self.c.post("/comments/" + self.test_comments[6] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data3, response_dict)

        for i in range(13):
            self.c.post("/comments/" + self.test_comments[5] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data4, response_dict)

        for i in range(13):
            self.c.post("/comments/" + self.test_comments[4] + "/ABC")
        response = self.c.get('/top/')
        response_dict = json.loads(response.content)
        self.assertDictEqual(self.test_data5, response_dict)
