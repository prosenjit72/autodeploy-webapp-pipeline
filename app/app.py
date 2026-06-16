from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os
##Python এর built-in database library, যা lightweight এবং serverless, self-contained, 
# এবং zero-configuration database eর জন্য ব্যবহৃত হয়। 
import socket 
## socket holo python er ekta built-in library jar maddhome amra network related kaj korte pari. socket er maddhome amra server er IP address and port number ber korte pari.
## আমরা একটা না, একাধিক container এ এই app চালাবো (horizontal scaling), তখন দেখতে চাইবো — প্রতিবার page refresh করলে কোন container request handle করছে। এটা scaling বোঝার জন্য খুব ভালো একটা visual indicator।
app = Flask(__name__)
##আমার Flask application শুরু হলো, এর নাম app
DB_NAME = os.path.join("data","tasks.db")
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)")
    conn.commit()
    conn.close()
    ##এই function টা database initialize করার জন্য, যদি database file না থাকে তাহলে 
    # এটা create করবে এবং একটা table তৈরি করবে যার নাম tasks, এই table এ id এবং 
    # content নামের দুইটা column থাকবে।
def get_tasks(): ##এই function টা database থেকে সব task গুলো fetch করে return করবে।
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def add_task(content): ##এই function টা database এ একটা নতুন task add করবে, content parameter হিসেবে task এর content নিবে।
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def delete_task(task_id): ##এই function টা database থেকে একটা task delete করবে, task_id parameter হিসেবে task এর id নিবে।
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

@app.route('/')
def home():
    hostname = socket.gethostname()
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks, hostname=hostname)
##এই route টা home page এর জন্য, যখন user home page এ যাবে তখন get_tasks() function call হবে এবং database থেকে সব task গুলো fetch করে index.html template এ পাঠানো হবে।

@app.route('/add', methods=['POST']) ##এই route টা নতুন task add করার জন্য, যখন user একটা নতুন task add করবে তখন এই route call হবে এবং request থেকে task content নিবে এবং add_task() function call করে database এ save করবে।
def add():
    task = request.form.get('task') ##request.form.get('task') এর মাধ্যমে user এর form থেকে task content নেওয়া হচ্ছে।
    if task: ##যদি task content থাকে তাহলে add_task() function call করে database এ save করা হবে।
        add_task(task)
    return redirect(url_for('home')) ##task add করার পর user কে আবার home page এ redirect করা হবে। 
@app.route('/delete/<int:task_id>') ##এই route টা task delete করার জন্য, যখন user একটা task delete করবে তখন এই route call হবে এবং URL থেকে task_id নিবে এবং delete_task() function call করে database থেকে delete করবে।
def delete(task_id):
    delete_task(task_id) ##delete_task() function call করে database থেকে task delete করা হবে।
    return redirect(url_for('home')) ##task delete করার পর user కে आबार home page ए redirect करा हবे
@app.route('/health') ##এই route টা application এর health check করার जन्य, यखन user एই route ए याबे तখন एटा एকটা JSON response return करবे यার मধ্যে status: ok थাকবে। एटा application एर health check कরार जन्य खूबই useful, बिशेष करे यखन आमरा एই app के Kubernetes ए deploy करবो तখন Kubernetes एই route टा use करे application एर health check कরবে।
def health():
    return jsonify({"status": "ok"})
if __name__ == '__main__': ##এই block টা check করে যে এই script টা main program হিসেবে run হচ্ছে কিনা, যদি হ্যাঁ তাহলে init_db() function call করে database initialize করা হবে এবং app.run() function call করে Flask application start করা হবে।
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True) ##app.run() function এর માધ્યમે Flask application start કરાશે, host='0.0.0.0' એર માધ્યમે application સવ IP address થી access કરાશે, port=5000 એર માધ્યમે application 5000 port એ run કરાશે, debug=True એર માધ્યમે application debug mode એ run કરાશે જ્યાં development એર જન્ય useful।