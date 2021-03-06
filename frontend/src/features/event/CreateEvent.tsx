import { QuestionCircleOutlined } from '@ant-design/icons'
import {
  Button,
  Form,
  Input,
  InputNumber,
  Radio,
  Select,
  Slider,
  Space,
  Steps,
  Tooltip,
  Upload,
} from 'antd'
import { FormInstance } from 'antd/es/form/Form'
import { useEffect, useState } from 'react'
import { useParams } from 'react-router'
import { useSearchParams } from 'react-router-dom'
import {
  brontoApi,
  useCreateEventMutation,
  useGetOrganizedEventQuery,
  useUpdateEventMutation,
} from '../../app/services/bronto'
import { CreateEventRequest } from '../../app/services/bronto-types'
import { html2plaintext } from '../../helpers'
import { Person } from '../person/types'
import DateRangeStringPicker from './DateRangeStringPicker'
import EditLocation from './EditLocation'
import { QualifiedPersonLabel } from './PersonOptionLabel'
import { getIsQualified } from './qualifications'
import RichTextEditor from './RichTextEditor'
import SelectAdministrativeUnit from './SelectAdministrativeUnit'
import SelectPerson from './SelectPerson'
import TimeStringPicker from './TimeStringPicker'
import {
  audiences,
  basicPurposes,
  diets,
  EventProps,
  eventTypes,
  NullableEventProps,
  programs,
  registrationMethods,
} from './types'

const getStepStatus = (
  form: FormInstance<FormEventProps>,
  items: string[],
): 'finish' | 'error' | 'wait' => {
  const states = items.map(name => {
    if (!form.getFieldInstance(name)) return 'none'
    else if (form.getFieldError(name).length > 0) return 'error'
    else if (form.isFieldTouched(name)) return 'touched'
  })
  if (states.every(state => state === 'touched')) return 'finish'
  if (states.includes('error')) return 'error'
  else return 'finish'
}
/*
const isItemValid = function (
  name: string,
  form: FormInstance<BeforeEventProps>,
  initialData: unknown,
) {
  const itemExists = !!form.getFieldInstance(name)
  const isItemTouched = form.isFieldTouched(name)
  const hasItemErrors = form.getFieldError(name).length > 0

  // success
  // item doesn't exist (nothing to validate)
  // OR
  // item exists and doesn't have errors AND (is touched OR is not required)
  // because we want every required field touched
  const isValid = !itemExists || (!hasItemErrors && isItemTouched)

  return isValid
}

const isStepValid = function <T>(
  step: Extract<keyof T, string>[],
  formConfig: FormConfig<T, never>,
  form: FormInstance<T>,
  initialData: unknown,
) {
  return step.every(name => isItemValid(name, formConfig, form, initialData))
}
*/

type FormEventProps = Partial<
  Omit<EventProps, 'dateFrom' | 'dateTo' | 'ageFrom' | 'ageTo' | 'location'> & {
    dateFromTo: [string, string]
    age: [number, number]
    location: [number, number]
  }
> & { name: string }

const reshapeForward = ({
  dateFrom,
  dateTo,
  ageFrom,
  ageTo,
  location,
  ...event
}: NullableEventProps): FormEventProps =>
  Object.fromEntries(
    Object.entries({
      dateFromTo: dateFrom && dateTo ? [dateFrom, dateTo] : undefined,
      age: [ageFrom, ageTo],
      location:
        location && location.gpsLatitude && location.gpsLongitude
          ? [location.gpsLatitude, location.gpsLongitude]
          : undefined,
      ...event,
    }).filter(([, value]) => value !== null),
  ) as FormEventProps

const reshapeReverse = ({
  dateFromTo,
  age,
  location, // eslint-disable-line @typescript-eslint/no-unused-vars
  eventType, // eslint-disable-line @typescript-eslint/no-unused-vars
  ...event
}: FormEventProps): CreateEventRequest => {
  return {
    dateFrom: dateFromTo?.[0],
    dateTo: dateFromTo?.[1],
    ageFrom: age?.[0],
    ageTo: age?.[1],
    ...event,
  }
}

const CreateEvent = () => {
  const [step, setStep] = useState(0)
  const [form] = Form.useForm<FormEventProps>()
  const eventId = Number(useParams()?.eventId ?? -1)
  const cloneEventId = Number(useSearchParams()[0].get('cloneEvent') ?? -1)

  const { isLoading, data: event } = useGetOrganizedEventQuery(
    eventId >= 0 ? eventId : cloneEventId,
  )

  const [triggerGetPerson] = brontoApi.useLazyGetPersonQuery()

  const [createEvent] = useCreateEventMutation()
  const [updateEvent] = useUpdateEventMutation()

  const isUpdating = eventId > 0

  useEffect(() => {
    if (event) {
      form.setFieldsValue(reshapeForward(event))
      form.validateFields()
    }
  }, [event, form])

  if (isLoading) return <div>Loading</div>

  const steps = [
    {
      title: 'Druh',
      element: (
        <Form.Item name="basicPurpose" rules={[{ required: true }]}>
          <Radio.Group>
            <Space direction="vertical">
              {Object.entries(basicPurposes).map(([value, name]) => (
                <Radio.Button value={value} key={value}>
                  {name}
                </Radio.Button>
              ))}
            </Space>
          </Radio.Group>
        </Form.Item>
      ),
      items: ['basicPurpose'],
    },
    {
      title: 'Typ',
      element: (
        <>
          <Form.Item
            name="eventType"
            label="Typ akce"
            rules={[{ required: true }]}
          >
            <Select>
              {Object.entries(eventTypes).map(([value, label]) => (
                <Select.Option key={value} value={value}>
                  {label}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="program"
            label="Program"
            rules={[{ required: true }]}
          >
            <Select>
              {Object.entries(programs).map(([value, name]) => (
                <Select.Option key={value} value={value}>
                  {name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item
            name="administrativeUnit"
            label="Po????daj??c?? Z??/Klub/RC/??st??ed??"
            rules={[{ required: true }]}
          >
            <SelectAdministrativeUnit />
          </Form.Item>
          <Form.Item
            name="intendedFor"
            label="Pro koho"
            tooltip="vyberte na koho je akce zam????en??"
            rules={[{ required: true }]}
          >
            <Select>
              {Object.entries(audiences).map(([value, name]) => (
                <Select.Option key={value} value={value}>
                  {name}
                </Select.Option>
              ))}
            </Select>
          </Form.Item>
          <Form.Item shouldUpdate>
            {() =>
              form.getFieldValue('intendedFor') === 'newcomers' ? (
                <>
                  <small>
                    <p className="mb-4">
                      Hnut?? Brontosaurus pravideln?? vytv?????? nab??dku v??b??rov??ch
                      dobrovolnick??ch akc??, kter??mi oslovujeme nov?? ????astn??ky,
                      zejm??na st??edo??kolskou ml??de?? a za????naj??c?? vysoko??kol??ky
                      (15 - 26 let). C??lem akce je oslovit tyto prvo????astn??ky a
                      m??t jich nejl??pe polovinu, (min. t??etinu) z celkov??ho
                      po??tu ????astn??k??.
                    </p>
                    <p className="mb-4">
                      Zad??n??m akce pro prvo????astn??ky z??sk??te:
                    </p>
                    <p className="mb-4">
                      <ul className="list-disc ml-6">
                        <li>
                          ??ir???? propagaci skrze let??ky, osobn?? kontakty apod.
                          Zve??ejn??n?? na let??ku VIP propagace.
                        </li>
                        <li>
                          Propagaci na programech pro st??edn?? ??koly - lekto??i
                          budou osobn?? na akce zv??t.
                        </li>
                        <li>
                          Zve??ejn??n?? na Facebooku a Instagramu HB a reklamu na
                          Facebooku
                        </li>
                        <li>Reklamu v Google vyhled??v??n??</li>
                        <li>Slu??by grafika HB (dle dohodnut??ho rozsahu)</li>
                        <li>P??id??n?? do webov??ch katalog?? akc?? </li>
                        <li>Slevu na inzerci v Roversk??m kmenu (pro t??bory)</li>
                        <li>Zp??tnou vazbu k webu a Facebooku akce</li>
                        <li>Metodickou pomoc a pomoc s agendou akce</li>
                        <li>Propagace na nov??m webu HB v sekci Jedu poprv??</li>
                      </ul>
                    </p>
                  </small>

                  <Form.Item
                    name="newcomerText1"
                    label="C??le akce a p????nos pro prvo????astn??ky"
                    tooltip="Jak?? je hlavn?? t??ma va???? akce? Jak?? jsou hlavn?? c??le akce? Co nejv??sti??n??ji popi??te, co akce p??in?????? ????astn??k??m, co zaj??mav??ho si zkus??, co se dozv??, nau????, v ??em se rozvinou???"
                  >
                    <Input.TextArea />
                  </Form.Item>

                  <Form.Item
                    name="newcomerText2"
                    label="Programov?? pojet?? akce pro prvo????astn??ky"
                    tooltip="V z??kladu uve??te, jak bude va??e akce programov?? a dramaturgicky koncipov??na (motiva??n?? p????b??h, zam????en?? programu ??? hry, diskuse, ??emesla,...). Uve??te, jak n??pl?? a program akce reflektuj?? pot??eby va???? c??lov?? skupiny prvo????astn??k??."
                  >
                    <Input.TextArea />
                  </Form.Item>

                  <Form.Item
                    name="newcomerText3"
                    label="Kr??tk?? zvac?? text do propagace"
                    tooltip="Ve 2-4 v??t??ch nal??kejte na va??i akci a zd??razn??te osobn?? p????nos pro ????astn??ky (max. 200 znak??)"
                    rules={[
                      {
                        max: 200,
                        message: 'max 200 znak??',
                      },
                    ]}
                  >
                    <Input.TextArea />
                  </Form.Item>
                </>
              ) : null
            }
          </Form.Item>
        </>
      ),
      items: [
        'eventType',
        'program',
        'administrativeUnit',
        'intendedFor',
        'newcomerText1',
        'newcomerText2',
        'newcomerText3',
      ],
    },
    {
      title: 'Info',
      element: (
        <>
          <Form.Item name="name" label="N??zev" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item
            name="dateFromTo"
            label="Od - Do"
            rules={[{ required: true }]}
          >
            <DateRangeStringPicker />
          </Form.Item>
          <Form.Item
            name="startTime"
            label="Za????tek akce"
            rules={[{ required: true }]}
          >
            <TimeStringPicker />
          </Form.Item>
          <Form.Item
            name="repetitions"
            label="Po??et akc?? v uveden??m obdob??"
            tooltip="Pou????v?? se u opakovan??ch akc?? (nap??. odd??lov?? sch??zky). U klasick?? jednor??zov?? akce zde nechte jedni??ku."
            rules={[{ required: true }]}
          >
            <InputNumber />
          </Form.Item>
        </>
      ),
      items: ['name', 'dateFromTo', 'startTime', 'repetitions'],
    },
    {
      title: 'M??sto',
      element: (
        <>
          <Form.Item shouldUpdate>
            {() => (
              <Form.Item
                name="location"
                label="Vybrat m??sto akce na map??"
                required={form.getFieldValue('basicPurpose') === 'camp'}
              >
                <EditLocation className="h-56 w-56" />
              </Form.Item>
            )}
          </Form.Item>
          <Form.Item
            name="locationInfo"
            label="M??sto kon??n?? akce"
            tooltip="n??zev/popis m??sta, kde se akce kon??"
            rules={[{ required: true }]}
          >
            <Input.TextArea />
          </Form.Item>
        </>
      ),
      items: ['location', 'locationInfo'],
    },

    {
      title: 'T??m',
      element: (
        <>
          <Form.Item shouldUpdate>
            {() => (
              <Form.Item
                name="mainOrganizer"
                label="Hlavn?? organiz??tor/ka"
                tooltip="Hlavn?? organiz??tor mus?? m??t n??le??it?? kvalifikace a za celou akci zodpov??d??. Je nutn?? zad??vat hlavn??ho organiz??tora do BIS p??ed akc??, aby m??l automaticky sjednan?? poji??t??n?? odpov??dnosti za ??kodu a ??razov?? poji??t??n??."
                rules={[
                  { required: true },
                  ({ getFieldValue }) => ({
                    validator: async (_, personId) => {
                      const intendedFor = getFieldValue('intendedFor')
                      const eventType = getFieldValue('eventType')
                      const basicPurpose = getFieldValue('basicPurpose')
                      if (!basicPurpose)
                        throw new Error('Vypl??te nejd????v Druh akce')
                      if (!eventType)
                        throw new Error('Vypl??te nejd????v Typ akce')
                      if (!intendedFor)
                        throw new Error(
                          'Vypl??te nejd????v Pro koho je akce ur??ena',
                        )
                      // get the person by id
                      if (!personId) return
                      const person = await triggerGetPerson(
                        personId,
                        true,
                      ).unwrap()
                      if (!person) throw new Error('??lov??k nenalezen')
                      const isQualified = getIsQualified(
                        { basicPurpose, eventType, intendedFor },
                        person.qualifications,
                      )
                      if (!isQualified)
                        throw new Error(
                          `${person.givenName} ${person.familyName} nem?? dostate??nou kvalifikaci`,
                        )
                    },
                  }),
                ]}
              >
                <SelectPerson
                  LabelComponent={QualifiedPersonLabel}
                  getDisabled={(person: Person) =>
                    !getIsQualified(
                      {
                        basicPurpose: form.getFieldValue('basicPurpose'),
                        eventType: form.getFieldValue('eventType'),
                        intendedFor: form.getFieldValue('intendedFor'),
                      },
                      person.qualifications,
                    )
                  }
                />
              </Form.Item>
            )}
          </Form.Item>
          <Form.Item
            name="team"
            label="Organiza??n?? t??m"
            tooltip="Vyberte jm??na dal????ch organiz??tor??. Organiz??tory je mo??n?? je??t?? p??ipojistit na ??razov?? poji??t??n?? a poji??t??n?? odpov??dnosti za ??kodu."
          >
            <SelectPerson multiple />
          </Form.Item>
        </>
      ),
      items: ['mainOrganizer', 'team'],
    },
    {
      title: 'Registrace',
      element: (
        <>
          <Form.Item
            name="registrationMethod"
            label="Zp??sob p??ihl????en??"
            tooltip="Zp??soby p??ihl????en?? na va??i akci na www.brontosaurus.cz, kter?? se zobraz?? po kliknut?? na tla????tko ???chci jet???"
            rules={[{ required: true }]}
          >
            <Select>
              {Object.entries(registrationMethods).map(
                ([value, { label, help }]) => (
                  <Select.Option key={value} value={value} tooltip={help}>
                    <span className="flex items-center gap-1">
                      {label}{' '}
                      <Tooltip title={help}>
                        <QuestionCircleOutlined className="cursor-help" />
                      </Tooltip>
                    </span>
                  </Select.Option>
                ),
              )}
            </Select>
          </Form.Item>
          <Form.Item shouldUpdate>
            {() => {
              switch (form.getFieldValue('registrationMethod')) {
                case 'other_electronic':
                  return (
                    <Form.Item
                      name="entryFormUrl"
                      label="Odkaz na elektronickou p??ihl????ku"
                      rules={[{ required: true }]}
                    >
                      <Input />
                    </Form.Item>
                  )
                case 'by_email':
                  return (
                    <Form.Item
                      name="registrationMethodEmail"
                      label="P??ihla??ovac?? email"
                      rules={[{ required: true }]}
                    >
                      <Input type="email" />
                    </Form.Item>
                  )
                case 'standard':
                  return [1, 2, 3, 4].map(i => (
                    <Form.Item
                      key={i}
                      name={`additionalQuestion${i}`}
                      label={`Ot??zka ${i}`}
                      tooltip="Zde m????e?? p??ipsat svoje dopl??uj??c?? ot??zky pro ????astn??ky, kter?? se zobraz?? u standardn?? p??ihl????ky na brontowebu"
                      rules={[{ required: true }]}
                    >
                      <Input />
                    </Form.Item>
                  ))
                default:
                  return null
              }
            }}
          </Form.Item>
        </>
      ),
      items: [
        'registrationMethod',
        'registrationMethodEmail',
        'entryFormUrl',
        'additionalQuestion1',
        'additionalQuestion2',
        'additionalQuestion3',
        'additionalQuestion4',
        'additionalQuestion5',
        'additionalQuestion6',
        'additionalQuestion7',
        'additionalQuestion8',
      ],
    },
    {
      title: 'Podrobnosti',
      element: (
        <>
          <Form.Item
            name="targetMembers"
            label="Na koho je akce zam????en??"
            tooltip="Akce zam????en?? na ??leny jsou intern?? akce HB - valn?? hromady, t??movky atd."
            rules={[{ required: true }]}
          >
            <Radio.Group
              options={[
                { label: 'Na ??leny', value: true },
                { label: 'Na ne??leny', value: false },
              ]}
              optionType="button"
            />
          </Form.Item>
          <Form.Item shouldUpdate>
            {() =>
              form.getFieldValue('basicPurpose') === 'camp' ? (
                <Form.Item
                  name="advertiseInRoverskyKmen"
                  label="Propagovat akci v Roversk??m kmeni"
                  tooltip="Placen?? propagace va???? v??cedenn?? akce v ??asopisu Roversk?? kmen za poplatek 100 K??."
                  rules={[{ required: true }]}
                >
                  <Radio.Group
                    options={[
                      { label: 'Ano', value: true },
                      { label: 'Ne', value: false },
                    ]}
                    optionType="button"
                  />
                </Form.Item>
              ) : null
            }
          </Form.Item>
          <Form.Item
            name="advertiseInBrontoWeb"
            label="Zve??ejnit na brontosau????m webu"
            tooltip="Pokud za??krtnete ano, akce se zobraz?? na webu www. brontosaurus.cz. Volbu ne za??krtn??te pouze jedn??-li se o intern?? akci HB nebo intern?? akci Br??a."
            rules={[{ required: true }]}
          >
            <Radio.Group
              options={[
                { label: 'Ano', value: true },
                { label: 'Ne', value: false },
              ]}
              optionType="button"
            />
          </Form.Item>
          <Form.Item
            name="participationFee"
            label="????astnick?? poplatek (CZK)"
            tooltip="Napi??te pouze ????stku, znak K?? se na webu zobraz?? automaticky. Pokud m??te v??ce druh?? poplatk??, jejich v????i napi??te za lom??tko nap??. 150/200/250"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item name="age" label="V??k" rules={[{ required: true }]}>
            <Slider range defaultValue={[0, 100]} marks={{ 0: 0, 100: 100 }} />
          </Form.Item>
          <Form.Item shouldUpdate>
            {() =>
              ['camp', 'action-with-attendee-list'].includes(
                form.getFieldValue('basicPurpose'),
              ) && (
                <>
                  <Form.Item
                    name="accommodation"
                    label="Ubytov??n??"
                    rules={[{ required: true }]}
                  >
                    <Input />
                  </Form.Item>

                  <Form.Item
                    name="diet"
                    label="Strava"
                    rules={[{ required: true }]}
                  >
                    <Select mode="multiple">
                      {Object.entries(diets).map(([value, name]) => (
                        <Select.Option key={value} value={value}>
                          {name}
                        </Select.Option>
                      ))}
                    </Select>
                  </Form.Item>
                </>
              )
            }
          </Form.Item>
          <Form.Item shouldUpdate>
            {() =>
              form.getFieldValue('basicPurpose') === 'camp' && (
                <>
                  <Form.Item name="workingHours" label="Pracovn?? doba">
                    <InputNumber />
                  </Form.Item>
                  <Form.Item
                    name="workingDays"
                    label="Po??et pracovn??ch dn?? na akci"
                  >
                    <InputNumber />
                  </Form.Item>
                </>
              )
            }
          </Form.Item>
        </>
      ),
      items: [
        'targetMembers',
        'advertiseInRoverskyKmen',
        'advertiseInBrontoWeb',
        'participationFee',
        'age',
        'accommodation',
        'diet',
        'workingHours',
        'workingDays',
      ],
    },
    {
      title: 'Kontakt',
      element: (
        <>
          <Form.Item
            name="contactPersonName"
            label="Jm??no kontaktn?? osoby"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="contactPersonEmail"
            label="Kontaktn?? email"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item name="contactPersonTelephone" label="Kontaktn?? telefon">
            <Input />
          </Form.Item>
          <Form.Item
            name="webUrl"
            label="Web o akci"
            tooltip="Mo??nost p??idat odkaz na webovou str??nku va???? akce."
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="note"
            label="Pozn??mka"
            tooltip="vid?? jenom lid?? s p????stupem do BISu, kte???? si akci prohl????ej?? p????mo v syst??mu"
          >
            <Input.TextArea />
          </Form.Item>
        </>
      ),
      items: [
        'contactPersonName',
        'contactPersonEmail',
        'contactPersonTelephone',
        'webUrl',
        'note',
      ],
    },
    {
      title: 'Pozv??nka',
      element: (
        <>
          <Form.Item
            name="invitationText1"
            label="Zvac?? text: Co n??s ??ek??"
            tooltip="Prvn??ch n??kolik v??t se zobraz?? v p??ehledu akc?? na webu. Prvn?? v??ty jsou k upout??n?? pozornosti nejd??le??it??j????, proto se na n?? zam????te a shr??te na co se ????astn??ci mohou t????it."
            required
            rules={[
              {
                validator: async (_, html) => {
                  if (html2plaintext(html).trim().length === 0)
                    throw new Error('Pole je povinn??')
                },
              },
            ]}
          >
            <RichTextEditor />
          </Form.Item>

          <Form.Item
            name="invitationText2"
            label="Zvac?? text: Co, kde a jak"
            required
            rules={[
              {
                validator: async (_, html) => {
                  if (html2plaintext(html).trim().length === 0)
                    throw new Error('Pole je povinn??')
                },
              },
            ]}
          >
            <RichTextEditor />
          </Form.Item>

          <Form.Item shouldUpdate>
            {() => (
              <Form.Item
                name="invitationText3"
                label="Zvac?? text: dobrovolnick?? pomoc"
                required={form.getFieldValue('eventType') === 'pracovni'}
                rules={[
                  ({ getFieldValue }) => ({
                    validator: async (_, html) => {
                      if (getFieldValue('eventType') !== 'pracovni') return
                      if (html2plaintext(html).trim().length === 0)
                        throw new Error('Pole je povinn??')
                    },
                  }),
                ]}
              >
                <RichTextEditor />
              </Form.Item>
            )}
          </Form.Item>

          <Form.Item
            name="invitationText4"
            label="Zvac?? text: Mal?? ochutn??vka"
            required
            tooltip="Mal?? ochutn??vka uv??d?? fotky, kter?? k akci p??ilo????te"
            rules={[
              {
                validator: async (_, html) => {
                  if (html2plaintext(html).trim().length === 0)
                    throw new Error('Pole je povinn??')
                },
              },
            ]}
          >
            <RichTextEditor />
          </Form.Item>

          <Form.Item
            name="mainPhoto"
            label="Hlavn?? foto"
            tooltip="Hlavn?? foto se zobraz?? v n??hledu akce na webu"
            rules={[{ required: true }]}
          >
            <Upload listType="picture-card">+</Upload>
          </Form.Item>
          {
            // @TODO or allow adding url to a picture
          }
          <Form.Item
            name="additionalPhotos"
            label="Fotky k mal?? ochutn??vce"
            tooltip="Dal???? fotky, kter?? se zobraz?? u akce."
          >
            <Upload listType="picture-card">+</Upload>
          </Form.Item>
          {
            // @TODO or allow adding url to a picture
          }
        </>
      ),
      items: [
        'invitationText1',
        'invitationText2',
        'invitationText3',
        'invitationText4',
        'mainPhoto',
        'additionalPhotos',
      ],
    },
  ]

  const validateMessages = {
    required: "Pole '${label}' je povinn??!",
  }

  const handleFinish = (formValues: FormEventProps) => {
    const values = reshapeReverse(formValues)
    if (isUpdating) {
      updateEvent({ ...values, id: eventId })
    } else {
      createEvent(values)
    }
  }

  return (
    <Form<FormEventProps>
      onFinish={handleFinish}
      form={form}
      layout="vertical"
      validateMessages={validateMessages}
      onValuesChange={value => {
        // if any of the following fields change
        // (intendedFor, eventType, basicPurpose)
        // validate mainOrganizer again
        // because their qualification requirements may have changed
        if (
          ['intendedFor', 'eventType', 'basicPurpose'].some(key =>
            Object.keys(value).includes(key),
          )
        )
          form.validateFields(['mainOrganizer'])
      }}
      initialValues={event}
    >
      <Form.Item shouldUpdate>
        {() => (
          <Steps size="small" current={step} className="mb-8">
            {steps.map(({ title, items }, index) => (
              <>
                <Steps.Step
                  title={title}
                  key={index}
                  onStepClick={i => setStep(i)}
                  status={
                    index === step ? 'process' : getStepStatus(form, items)
                  }
                />
              </>
            ))}
          </Steps>
        )}
      </Form.Item>
      {steps.map(({ element }, index) => (
        <div key={index} className={index !== step ? 'hidden' : undefined}>
          {element}
        </div>
      ))}
      <div className="steps-action">
        {step > 0 && (
          <Button
            style={{ margin: '0 8px' }}
            onClick={() => setStep(step => step - 1)}
          >
            Zp??t
          </Button>
        )}
        {step < steps.length - 1 && (
          <Button type="primary" onClick={() => setStep(step => step + 1)}>
            D??l
          </Button>
        )}
        {step === steps.length - 1 && (
          <Button type="primary" htmlType="submit">
            Hotovo
          </Button>
        )}
      </div>
    </Form>
  )
}

export default CreateEvent
