import unittest
import random
import string
import wunderpy2

import tests_config
from endpoint_test_case import EndpointTestCase


class TestTasksEndpoint(EndpointTestCase):
    def setUp(self):
        ''' Does normal endpoint setup and also sets up tracking of any tasks that were created during the course of testing '''
        super(TestTasksEndpoint, self).setUp()
        self._tasks_ids_to_cleanup = set()

    def tearDown(self):
        ''' Cleans up any tasks created in the course of testing '''
        for task_id in self._tasks_ids_to_cleanup:
            try:
                _, task_obj = self.client.get_task(task_id)
                revision = task_obj[wunderpy2.model.Task.REVISION]
                self.client.delete_task(task_id, revision)
            except ValueError:
                continue

    def _get_test_task(self):
        ''' Creates a new task with a random ID that gets cleaned up after the test is run '''
        random_title = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        # TODO It's not ideal that this depends on the 'create_task' function which is getting testsed, but the alternative is to re-implement task-creating logic,
        #  which is very fragile in case any of the Wunderlist stuff changes
        code, new_task = self.client.create_task(tests_config.TasksEndpointCfgValues.LIST_ID, random_title)
        assert code == 201
        self._tasks_ids_to_cleanup.add(new_task[wunderpy2.model.Task.ID])
        return new_task

    def test_get_tasks(self):
        code, resp = self.client.get_tasks(tests_config.TasksEndpointCfgValues.LIST_ID)
        self.assertEqual(code, 200)

    def test_get_completed_tasks(self):
        code, _ = self.client.get_completed_tasks(tests_config.TasksEndpointCfgValues.LIST_ID, True)
        self.assertEqual(code, 200)

    def test_get_uncompleted_tasks(self):
        code, _ = self.client.get_completed_tasks(tests_config.TasksEndpointCfgValues.LIST_ID)
        self.assertEqual(code, 200)

    # Try creating a task with a non-existent list
    def test_create_task_with_nonexist_list(self):
        code, response = self.client.create_task(tests_config.TasksEndpointCfgValues.LIST_ID_NONEXIST, title="TASK-IN-NON-EXISTENT-LIST")
        self.assertEqual(code, 201)

    # Try creating a task with a task with a string for list ID
    def test_create_task_with_exist_list(self):
        code, new_task = self.client.create_task(tests_config.TasksEndpointCfgValues.LIST_ID, title="TASK-IN-EXISTENT-LIST")
        self.assertEqual(code, 201)
        self._tasks_ids_to_cleanup.add(new_task[wunderpy2.model.Task.ID])

    # Try creating a task with too long of a title
    def test_create_task_with_invalid_title(self):
        title = 'TEST' * 70
        code, new_task = self.client.create_task(tests_config.TasksEndpointCfgValues.LIST_ID, title=title)
        self.assertRaises(ValueError, lambda _: print "value error")

    # Updating task...
    def test_update_task(self):
        task = self._get_test_task()
        code, resp = self.client.update_task(
                task[wunderpy2.model.Task.ID],
                task[wunderpy2.model.Task.REVISION],
                title = "UPDATE TASK"
            )
        self.assertEqual(code, 200)

    # updating a task with known out-of-date revision
    def test_update_task_outdate_revision(self):
        task = self._get_test_task()
        code, resp = self.client.update_task(
                task[wunderpy2.model.Task.ID],
                -1,
                title = "UPDATE TASK"
            )
        self.assertEqual(code, 409)
        self.assertRaises(ValueError, self.client.get_task(), task[wunderpy2.model.Task.ID])

    # Try updating a non-existent task ID
    def test_update_nonexist_task(self):
        code, resp = self.client.update_task(123, 1, "NOEXIST TASK")
        self.assertEqual(code, 404)
        self.assertRaises(ValueError, lambda _:print "valueerror")

    # Try updating a task with too long a title
    def test_update_task_with_invalid_title(self):
        title = "test"*70
        task = self._get_test_task()
        code, resp = self.client.update_task(
                task[wunderpy2.model.Task.ID],
                task[wunderpy2.model.Task.REVISION],
                title = title
            )
        self.assertRaises(ValueError, self.client.get_task, task[wunderpy2.model.Task.ID])

    # Try removing some properties from a task
    def test_update_task_with_remove_attr(self):
        task = self._get_test_task()
        code, resp = self.client.update_task(
                task[wunderpy2.model.Task.ID],
                task[wunderpy2.model.Task.REVISION],
                remove = ["due_date"]
            )
        self.assertEqual(code, 200)

    # Deleting task...
    def test_delete_task(self):
        task = self._get_test_task()
        code, resp = self.client.delete_task(
                task[wunderpy2.model.Task.ID],
                task[wunderpy2.model.Task.REVISION]
            )
        self.assertEqual(code, 204)


    # Try deleting a task with out-of-date revision
    def test_delete_task(self):
        task = self._get_test_task()
        code, resp = self.client.delete_task(
                task[wunderpy2.model.Task.ID],
                -1
            )
        self.assertEqual(code, 409)
        self.assertRaises(ValueError, self.client.get_task, task[wunderpy2.model.Task.ID])


if __name__ == "__main__":
    unittest.main()
