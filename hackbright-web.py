from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')
    # if github == 'None':
    #     return "Please request a valid github account in the form /student?github=[USERNAME]"
    try: 
        first, last, github = hackbright.get_student_by_github(github)

        grade_data = hackbright.get_grades_by_github(github)
    
        html = render_template("student_info.html", first=first,
                                                last=last,
                                                github=github,
                                                grade_data=grade_data)
    except TypeError:
        html = "This is not a valid student, <a href='/student-search'>please try again</a>."

    return html


@app.route("/student-add")
def form_add_student():
    """form to add a student to our database"""

    return render_template("student_add.html")


@app.route("/confirmation", methods=["POST"])
def add_student():
    """add student from form data to database, displays confirmation"""
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    return render_template("confirm.html", first=first_name, 
                                           last=last_name, 
                                           github=github)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
