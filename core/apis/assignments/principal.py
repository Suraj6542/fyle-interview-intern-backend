from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema  
from werkzeug.exceptions import BadRequest

# Define a Blueprint for principal assignments resources
principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)

# Route to list all submitted and graded assignments
@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of submitted and graded assignments"""
    # Query for assignments that are in 'SUBMITTED' or 'GRADED' state
    all_assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    # Serialize the assignments using AssignmentSchema
    all_assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    # Return the serialized data as a response
    return APIResponse.respond(data=all_assignments_dump)

# Route to list all teachers
@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_teachers(p):
    """Returns list of all teachers"""
    # Query for all teachers in the database
    all_teachers = Teacher.query.all()
    # Serialize the teachers using TeacherSchema
    all_teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    # Return the serialized data as a response
    return APIResponse.respond(data=all_teachers_dump)

# Route to grade or re-grade an assignment
@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def re_grade_assignment(p, incoming_payload: dict):
    """Grade or re-grade an assignment"""
    # Load and validate the incoming payload using AssignmentGradeSchema
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    # Fetch the assignment from the database by ID
    assignment = Assignment.query.get(grade_assignment_payload.id)

    # Check if the assignment is in 'DRAFT' state
    if assignment.state == 'DRAFT':
        raise BadRequest("The pricipal cannot modified the assignment from draft state !")

    # Update the assignment's grade and state
    assignment.grade = grade_assignment_payload.grade
    assignment.state = 'GRADED'
    # Commit the changes to the database
    db.session.commit()

    # Serialize the updated assignment using AssignmentSchema
    graded_assignment_dump = AssignmentSchema().dump(assignment)
    # Return the serialized data as a response
    return APIResponse.respond(data=graded_assignment_dump)
