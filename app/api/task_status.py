class TaskStatus:
    NOT_COMPLETED = "0"
    NOT_COMPLETED_EDITED = "1"
    COMPLETED = "10"
    COMPLETED_EDITED = "11"

    description = {
        NOT_COMPLETED: "Not completed",
        NOT_COMPLETED_EDITED: "Not completed, edited",
        COMPLETED: "Completed",
        COMPLETED_EDITED: "Completed, edited",
    }