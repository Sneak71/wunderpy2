import unittest
import wunderpy2

import tests_config
from endpoint_test_case import EndpointTestCase

class TestNotesEndpoint(EndpointTestCase):

    # Delete any leftover, hanging-around notes to return the state to what it was before we started
    @classmethod
    def setUpClass(cls):
        cls._leftover_notes = set()

    @classmethod
    def tearDownClass(cls):
        # Delete leftover notes here
        for note_id in cls._leftover_notes:
            try:
                _, note_obj = self.client.get_note(note_id)
                revision = note_id[wunderpy2.model.Note.REVISION]
                self.client.delete_note(note_id, revision)
            except Exception as e:
                pass

    def test_get_task_notes(self):
        code, resp = self.client.get_task_notes(tests_config.NotesEndpointCfgValues.TASK_ID_WITH_NOTES)
        print resp
        self.assertEqual(code, 200)

    def test_get_list_notes(self):
        code, _ = self.client.get_list_notes(tests_config.NotesEndpointCfgValues.LIST_ID)
        self.assertEqual(code, 200)

    def test_get_note(self):
        code, _ = task_notes = self.client.get_note(tests_config.NotesEndpointCfgValues.NOTE_ID)
        self.assertEqual(code, 200)

    ''' 
    Disabled for now as there's a bug in Wunderlist API where you have to 
    call DELETE twice for the note to actually get deleted
    '''
    def test_crud_note(self):
        # create
        code, new_note = self.client.create_note(tests_config.NotesEndpointCfgValues.TASK_ID_WITHOUT_NOTES, "DELETE")
        self.assertEqual(code, 201)
        new_note_id = new_note[wunderpy2.model.Note.ID]
        new_note_revision = new_note[wunderpy2.model.Note.REVISION]
        cls._leftover_notes.append(new_note_id)

        # read
        code, retrieved_note = self.client.get_note(new_note_id)
        self.assertEqual(code, 200)
        self.assertDictEqual(new_note, retrieved_note)

        # update
        new_content = "DELETEME"
        code, updated_note = self.client.update_note(new_note_id, new_note_revision, new_content)
        self.assertEqual(code, 200)
        updated_content = updated_note[wunderpy2.model.Note.CONTENT]
        updated_revision = updated_note[wunderpy2.model.Note.revision]
        self.assertEqual(new_content, updated_content)

        # delete
        code = self.client.delete_note(new_note_id, updated_revision)
        self.assertEqual(code, 204)
    #'''

if __name__ == "__main__":
    unittest.main()
