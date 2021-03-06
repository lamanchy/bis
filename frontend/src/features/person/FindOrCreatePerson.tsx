import { Button, Modal } from 'antd'
import { useState } from 'react'
import { wait } from '../../helpers'
import SelectPerson from '../event/SelectPerson'
import CreatePerson from './CreatePerson'
import { createPerson } from './personAPI'
import { NewPerson, Person } from './types'

/* // TODO these commented-out sections could be used elsewhere. We may need them!
// So we keep them here for future reference. May want to be removed before this project is done.
interface PersonData {
  givenName: string
  familyName: string
  birthdate: moment.Moment
}
*/

interface FindOrCreatePersonProps {
  onPerson: (person: Person) => void
}

export const FindOrCreatePerson = ({ onPerson }: FindOrCreatePersonProps) => {
  const [isUserModalVisible, setIsUserModalVisible] = useState(false)
  const [showUserSaved, setShowUserSaved] = useState(false)
  const [personId, setPersonId] = useState<number | []>([])

  /*
  const handleFinish = async ({
    givenName,
    familyName,
    birthdate: momentBirthdate,
  }: PersonData) => {
    const birthdate = momentBirthdate.format('YYYY-MM-DD')
    /** TODO figure out if we should put this whole thing to redux * /
    const person = await findPerson({ givenName, familyName, birthdate })

    if (person) {
      onPerson(person)
    }
  }
  */

  const handleSelectPerson = (person: Person) => {
    setPersonId([])
    onPerson(person)
  }

  const handleOk = () => {
    setIsUserModalVisible(false)
  }

  const handleCancel = () => {
    setIsUserModalVisible(false)
  }

  const handlePersonSubmit = async (personData: NewPerson) => {
    /** TODO:  we are not checking if user exists before adding them
    (for it to be done there is a need for info how to check for duplicates) */

    const newPerson = await createPerson(personData) // TODO let's consider connecting this to redux
    if (newPerson) {
      onPerson(newPerson)
    }
    setShowUserSaved(true) // TODO it would be also interesting to have some generic component that displays such info about success or failure
    await wait(1500)
    handleCancel()
    setShowUserSaved(false)
  }

  return (
    <>
      {/*
      <Form className="flex" onFinish={handleFinish}>
        <Form.Item name="givenName" rules={[{ required: true }]}>
          <Input placeholder="Jm??no" />
        </Form.Item>
        <Form.Item name="familyName" rules={[{ required: true }]}>
          <Input placeholder="P????jmen??" />
        </Form.Item>
        <Form.Item name="birthdate" rules={[{ required: true }]}>
          <DatePicker placeholder="Datum narozen??" />
        </Form.Item>
        <Form.Item>
          <Button htmlType="submit">P??idat</Button>
        </Form.Item>
      </Form>
    */}
      <SelectPerson
        placeholder="Zadej za????tek jm??na, p??ezd??vky nebo p????jmen??"
        className="flex"
        onPerson={handleSelectPerson}
        value={personId}
        defaultOption={
          <Button onClick={() => setIsUserModalVisible(true)}>
            ????astn??k nenalezen? Vytvo??it nov??ho ????astn??ka.
          </Button>
        }
      />
      <Modal
        title="Nov?? u??ivatel"
        visible={isUserModalVisible}
        footer={[]}
        onOk={handleOk}
        onCancel={handleCancel}
      >
        {!showUserSaved && <CreatePerson onSubmit={handlePersonSubmit} />}
        {showUserSaved && <div>Person added succesfully!</div>}
      </Modal>
    </>
  )
}
/**{{ display: 'inline-block', width: 'calc(50% - 8px)' }}*/
export default FindOrCreatePerson
