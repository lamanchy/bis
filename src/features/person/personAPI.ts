import { wait } from '../../helpers'
import { Person, NewPerson } from './types'

export const searchPeople = async (query: string): Promise<Person[]> => {
  if (query.length === 0) return []

  await wait(700)

  return fakePeople
}

export const findPerson = async ({
  givenName,
  familyName,
  birthdate,
}: {
  givenName: string
  familyName: string
  birthdate: string
}): Promise<Person | null> => {
  await wait(800)
  return birthdate === '2021-01-01'
    ? null
    : {
        id: Math.random(),
        givenName,
        familyName,
        nickname: '',
        qualifications: [],
      }
}

export const createPerson = async (
  personData: NewPerson,
): Promise<Person | null> => {
  await wait(800)
  const { nickname, givenName, familyName } = personData

  const person = {
    id: Math.random(),
    nickname,
    givenName,
    familyName,
    qualifications: [],
  }
  return personData.birthdate === '2021-01-01' ? null : person
}

export const fakePeople: Person[] = [
  {
    id: 1,
    nickname: 'Kos',
    givenName: 'Jana',
    familyName: 'Nováková',
    qualifications: ['OHB'],
  },
  {
    id: 2,
    nickname: 'Pavouk',
    givenName: 'Pavel',
    familyName: 'Němec',
    qualifications: [],
  },
  {
    id: 3,
    nickname: 'Květen',
    givenName: 'Hynek',
    familyName: 'Máj',
    qualifications: ['OvHB', 'OHB-BRĎO'],
  },
  {
    id: 4,
    nickname: 'Tráva',
    givenName: 'Vilém',
    familyName: 'Máchal',
    qualifications: ['OHB-BRĎO-P', 'Instruktor'],
  },
  {
    id: 5,
    nickname: '',
    givenName: 'Jarmila',
    familyName: 'Kotrbová',
    qualifications: ['OHB-BRĎO-P'],
  },
]
