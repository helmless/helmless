{{/*
Create the fully qualified image name.
*/}}
{{- define "helmless.image" -}}
{{- if typeIs "string" .Values.image }}
{{- .Values.image }}
{{- else }}
{{- if .Values.image.registry }}
{{- printf "%s/%s" .Values.image.registry .Values.image.repository }}
{{- else }}
{{- printf "%s" .Values.image.repository }}
{{- end }}
{{- if .Values.image.name }}
{{- printf "/%s" .Values.image.name }}
{{- end }}
{{- if .Values.image.tag }}
{{- printf ":%s" .Values.image.tag }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Generate the cross-project secrets annotation value.
*/}}
{{- define "helmless.crossProjectSecrets" -}}
{{- $crossProjectSecrets := list }}
{{- range $key, $value := . }}
{{- if and (not (typeIs "string" $value)) $value.project }}
{{- $crossProjectSecrets = append $crossProjectSecrets (printf "%s:projects/%s/secrets/%s" $key $value.project $value.secret) }}
{{- end }}
{{- end }}
{{- join "," $crossProjectSecrets }}
{{- end }}

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

{{/*
Build network interfaces configuration for Cloud Run
*/}}
{{- define "helmless.cloudrun.networkInterfaces" -}}
{{- if and .vpc .subnetwork -}}
{{ dict "network" .vpc "subnetwork" .subnetwork "tags" (.tags | default list) | toJson }}
{{- end -}}
{{- end -}}
