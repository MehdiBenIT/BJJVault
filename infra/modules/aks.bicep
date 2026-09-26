@description('Single-node AKS cluster (Free control-plane tier). Stop the cluster when idle: az aks stop.')
param location string
param namePrefix string
param logAnalyticsWorkspaceId string
param acrId string

@description('VM size for the single node. B2s is the cheapest burstable size that runs Kubernetes reliably.')
param nodeVmSize string = 'Standard_B2s'

resource aks 'Microsoft.ContainerService/managedClusters@2024-02-01' = {
  name: '${namePrefix}-aks'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  sku: {
    name: 'Base'
    tier: 'Free'
  }
  properties: {
    dnsPrefix: '${namePrefix}-aks'
    agentPoolProfiles: [
      {
        name: 'system'
        count: 1
        vmSize: nodeVmSize
        mode: 'System'
        osType: 'Linux'
        osDiskSizeGB: 30
        enableAutoScaling: false
        type: 'VirtualMachineScaleSets'
      }
    ]
    addonProfiles: {
      omsagent: {
        enabled: true
        config: {
          logAnalyticsWorkspaceResourceID: logAnalyticsWorkspaceId
        }
      }
    }
  }
}

// Grant AKS's kubelet identity AcrPull on the registry, so nodes can pull images without imagePullSecrets.
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acrId, aks.id, 'AcrPull')
  scope: resourceGroup()
  properties: {
    principalId: aks.properties.identityProfile.kubeletidentity.objectId
    principalType: 'ServicePrincipal'
    roleDefinitionId: subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')
  }
}

output aksName string = aks.name
output clusterFqdn string = aks.properties.fqdn
