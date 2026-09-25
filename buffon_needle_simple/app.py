"""Flask web interface for the Buffon's needle simulation.

The page calls /step, the server adds another batch of needles and returns the redrawn results.
"""

from flask import Flask, render_template, request

from buffon import add_throws, simulate, validate_parameters
from plots import convergence_image, needles_image, phase_space_image

STEPS_PER_RUN = 200  # number of steps needed to reach the target N

app = Flask(__name__)
experiment = None


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/step")
def step():
    global experiment
    try:
        n = int(request.form["n"])
        needle_length = float(request.form["needle_length"])
        line_spacing = float(request.form["line_spacing"])
    except ValueError:
        return {"error": "Zadejte čísla (desetinná s tečkou)."}, 400
    try:
        validate_parameters(n, needle_length, line_spacing)
    except ValueError as exc:
        return {"error": str(exc)}, 400

    batch = max(1, n // STEPS_PER_RUN)
    same_parameters = (experiment is not None
                       and experiment.needle_length == needle_length
                       and experiment.line_spacing == line_spacing)

    if same_parameters and experiment.n < n:
        experiment = add_throws(experiment, min(batch, n - experiment.n))
    else:
        experiment = simulate(batch, needle_length, line_spacing)

    html = render_template(
        "results.html",
        result=experiment,
        needles=needles_image(experiment),
        phase_space=phase_space_image(experiment),
        convergence=convergence_image(experiment),
    )
    return {"html": html, "done": experiment.n >= n}


if __name__ == "__main__":
    app.run(debug=True)
