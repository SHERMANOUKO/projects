package main

import(
	"database/sql"
	"log"
	"net/http"
	"github.com/gorilla/mux"
	"encoding/json"
	_"github.com/go-sql-driver/mysql"
	"io/ioutil"
)

type Post struct {
	ID string `json:"id"`
	Title string `json:"title"`
	Author string `json:"title"`
}

var db *sql.DB
var err error

func main(){
	//set up database coonection
	db, err = sql.Open("mysql", "sherman:sherman@tcp(127.0.0.1:3306)/posts")
	if err != nil {
		panic(err.Error())
	}

	defer db.Close()

	//initializing router
	router := mux.NewRouter()

	//creating endpoints
	router.HandleFunc("/posts", getPosts).Methods("GET")
	router.HandleFunc("/posts", createPost).Methods("POST")
	router.HandleFunc("/posts/{id}", getPost).Methods("GET")
	router.HandleFunc("/posts/{id}", updatePost).Methods("PUT")
	router.HandleFunc("/posts/{id}", deletePost).Methods("DELETE")

	log.Fatal(http.ListenAndServe(":8000", router))

}


func getPosts(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type","application/json")

	var posts []Post

	res, err := db.Query("SELECT * FROM posts")
	if err != nil {
		panic(err.Error())
	}

	defer res.Close()

	for res.Next() {
		var post Post
		err := res.Scan(&post.ID, &post.Title, &post.Title)
		if err != nil {
			panic(err.Error())
		}
		posts = append(posts, post)
	}

	json.NewEncoder(w).Encode(posts)
}

func getPost(w http.ResponseWriter, r *http.Request){
	w.Header().Set("Content-Type","application/json")
	params := mux.Vars(r)

	res, err := db.Query("SELECT * FROM posts WHERE id = ?", params["id"])
	if err != nil {
		panic(err.Error())
	}

	defer res.Close()

	var post Post

	for res.Next(){
		err := res.Scan(&post.ID, &post.Title, &post.Author)
		if err != nil {
			panic(err.Error())
		}
	}
	json.NewEncoder(w).Encode(post)
}

func createPost(w http.ResponseWriter, r *http.Request){
	stmt, err := db.Prepare("INSERT INTO posts(title, author) VALUES(?, ?)")
	if err != nil {
		panic(err.Error())
	}

	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		panic(err.Error())
	}

	keyVal := make(map[string]string)
	json.Unmarshal(body, &keyVal)
	title := keyVal["title"]
	author := keyVal["author"]

	_, err = stmt.Exec(title, author)
	if err != nil {
		panic(err.Error())
	}

	fmt.Fprintf(w, "New post was created")
}

func updatePost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)  
	stmt, err := db.Prepare("UPDATE posts SET title = ?, author = ? WHERE id = ?")
	
	if err != nil {
		panic(err.Error())
	}  
	
	body, err := ioutil.ReadAll(r.Body)
	
	if err != nil {
		panic(err.Error())
	}  
	
	keyVal := make(map[string]string)
	json.Unmarshal(body, &keyVal)
	newTitle := keyVal["title"]
	newAuthor := keyVal["author"]
	
	_, err = stmt.Exec(newTitle, newAuthor, params["id"])
	
	if err != nil {
		panic(err.Error())
	}  
	
	fmt.Fprintf(w, "Post with ID = %s was updated", params["id"])

}

func deletePost(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	stmt, err := db.Prepare("DELETE FROM posts WHERE id = ?")
	
	if err != nil {
		panic(err.Error())
	}  
	_, err = stmt.Exec(params["id"])
   
	if err != nil {
		panic(err.Error())
	}
	
	fmt.Fprintf(w, "Post with ID = %s was deleted", params["id"])
}

