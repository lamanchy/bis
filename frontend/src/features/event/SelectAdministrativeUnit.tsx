import { Select } from 'antd'
import { forwardRef } from 'react'
import { brontoApi } from '../../app/services/bronto'
import { match } from '../../helpers'
import {
  AdministrativeUnit,
  administrativeUnitLevel,
} from '../administrativeUnit/types'

type SelectProps = Parameters<typeof Select>[0]

const UnitLabel = ({ unit }: { unit: AdministrativeUnit }) => {
  const name = unit.name && <b>{unit.name}</b>
  const city = unit.city && <span>({unit.city})</span>
  const level = <i>{administrativeUnitLevel[unit.level]}</i>
  return (
    <span>
      {level} {name} {city}
    </span>
  )
}

const getTitle = (unit: AdministrativeUnit): string => {
  const infoItems: string[] = []
  if (unit.level) infoItems.push(administrativeUnitLevel[unit.level])
  if (unit.city) infoItems.push(unit.city)

  const info = infoItems.length === 0 ? '' : ` (${infoItems.join(' - ')})`

  return `${unit.name}${info}`
}

const SelectAdministrativeUnit = forwardRef<HTMLSelectElement, SelectProps>(
  (props, ref) => {
    const { data: administrativeUnits = [] } =
      brontoApi.useGetAdministrativeUnitsQuery()

    return (
      <Select
        ref={ref}
        showSearch
        {...props}
        options={administrativeUnits.map(unit => ({
          label: <UnitLabel unit={unit} />,
          title: getTitle(unit),
          value: unit.id,
        }))}
        filterOption={(inputValue, option) =>
          !!inputValue && match(option?.title, inputValue)
        }
      ></Select>
    )
  },
)

SelectAdministrativeUnit.displayName = 'SelectAdministrativeUnit'

export default SelectAdministrativeUnit
