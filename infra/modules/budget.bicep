// Deploy at subscription scope: az deployment sub create --location <region> --template-file infra/modules/budget.bicep
targetScope = 'subscription'

@description('Monthly cost budget with email alerts, so this stays cheap by construction, not by hoping.')
param namePrefix string
param budgetAmount int = 20
param alertEmail string
param startDate string = utcNow('yyyy-MM-01')

resource budget 'Microsoft.Consumption/budgets@2023-11-01' = {
  name: '${namePrefix}-monthly-budget'
  properties: {
    category: 'Cost'
    amount: budgetAmount
    timeGrain: 'Monthly'
    timePeriod: {
      startDate: startDate
    }
    notifications: {
      actual50: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 50
        contactEmails: [alertEmail]
        thresholdType: 'Actual'
      }
      actual90: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 90
        contactEmails: [alertEmail]
        thresholdType: 'Actual'
      }
      forecasted100: {
        enabled: true
        operator: 'GreaterThanOrEqualTo'
        threshold: 100
        contactEmails: [alertEmail]
        thresholdType: 'Forecasted'
      }
    }
  }
}
