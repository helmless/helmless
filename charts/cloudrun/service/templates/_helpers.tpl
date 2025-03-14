{{/*
Get CPU throttling value with proper defaults
*/}}
{{- define "helmless.cloudrun.cpuThrottling" -}}
{{- $cpuThrottling := "true" -}}
{{- if hasKey .Values "resources" -}}
  {{- if hasKey .Values.resources "cpuThrottling" -}}
    {{- $cpuThrottling = .Values.resources.cpuThrottling | toString -}}
  {{- end -}}
{{- end -}}
{{- $cpuThrottling -}}
{{- end -}}
