{{/*
Validate CPU settings and return error message if invalid
*/}}
{{- define "helmless.cloudrun.validateCPU" -}}
{{- if (lt (float64 ((.Values.resources).limits).cpu | default 1.0) 1.0) -}}
    {{- $wrongEnv := (ne (.Values.executionEnvironment | default "gen2") "gen1") -}}
    {{- $wrongConcurrency := (ne (int ((.Values.autoscaling).maxConcurrentRequests | default 80)) 1) -}}
    {{- $cpu := ((.Values.resources).limits).cpu -}}
    {{- $env := .Values.executionEnvironment | default "gen2" -}}
    {{- $concurrency := int ((.Values.autoscaling).maxConcurrentRequests | default 80) -}}

    {{- if (and $wrongEnv $wrongConcurrency) -}}
      {{- required "When using CPU < 1: maxConcurrentRequests must be set to 1 and execution environment must be gen1" nil -}}
    {{- else if $wrongEnv -}}
      {{- required "When using CPU < 1, you must use gen1 execution environment" nil -}}
    {{- else if $wrongConcurrency -}}
      {{- required "When using CPU < 1, maxConcurrentRequests must be set to 1" nil -}}
    {{- end -}}
{{- end -}}
{{- end -}}
