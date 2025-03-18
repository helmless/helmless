{{/*
Validate job parameters
*/}}
{{- define "helmless.cloudrun.job.validate" -}}
{{- include "helmless.cloudrun.validateVolumes" . -}}

{{- if and (hasKey . "Values") (hasKey .Values "parallelism") (hasKey .Values "taskCount") -}}
{{- if gt (int .Values.parallelism) (int .Values.taskCount) -}}
{{- fail (printf "Parallelism (%d) cannot exceed taskCount (%d)" (int .Values.parallelism) (int .Values.taskCount)) -}}
{{- end -}}
{{- end -}}

{{- if and (hasKey . "Values") (hasKey .Values "timeoutSeconds") -}}
{{- if lt (int .Values.timeoutSeconds) 1 -}}
{{- fail (printf "timeoutSeconds (%d) must be at least 1 second" (int .Values.timeoutSeconds)) -}}
{{- end -}}
{{- end -}}

{{- if and (hasKey . "Values") (hasKey .Values "maxRetries") -}}
{{- if lt (int .Values.maxRetries) 0 -}}
{{- fail (printf "maxRetries (%d) cannot be negative" (int .Values.maxRetries)) -}}
{{- end -}}
{{- end -}}

{{- if and (hasKey . "Values") (hasKey .Values "taskCount") -}}
{{- if lt (int .Values.taskCount) 1 -}}
{{- fail (printf "taskCount (%d) must be at least 1" (int .Values.taskCount)) -}}
{{- end -}}
{{- end -}}

{{- if and (hasKey . "Values") (hasKey .Values "parallelism") -}}
{{- if lt (int .Values.parallelism) 0 -}}
{{- fail (printf "parallelism (%d) cannot be negative" (int .Values.parallelism)) -}}
{{- end -}}
{{- end -}}
{{- end -}}
