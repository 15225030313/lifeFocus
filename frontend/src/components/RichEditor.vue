<template>
  <div class="rich-editor">
    <div class="toolbar">
      <button type="button" @mousedown.prevent="exec('bold')" title="加粗"><b>B</b></button>
      <button type="button" @mousedown.prevent="exec('italic')" title="斜体"><i>I</i></button>
      <button type="button" @mousedown.prevent="exec('insertUnorderedList')" title="列表">≡</button>
      <button type="button" @mousedown.prevent="exec('formatBlock', 'H3')" title="标题">H</button>
      <button type="button" @mousedown.prevent="insertImage" title="插入图片">🖼</button>
    </div>
    <div
      class="editor"
      contenteditable="true"
      ref="editorRef"
      @input="onInput"
      v-html="modelValue"
    ></div>
    <input ref="fileRef" type="file" accept="image/*" hidden @change="onFile" />
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { uploadImage } from '@/api'
import { API_BASE } from '@/utils/request'

const props = defineProps<{ modelValue: string }>()
const emit = defineEmits<{ (e: 'update:modelValue', v: string): void }>()
const editorRef = ref<HTMLElement>()
const fileRef = ref<HTMLInputElement>()

function exec(cmd: string, value?: string) {
  document.execCommand(cmd, false, value)
  onInput()
}
function onInput() {
  emit('update:modelValue', editorRef.value?.innerHTML || '')
}
function insertImage() {
  fileRef.value?.click()
}
async function onFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  try {
    const res: any = await uploadImage(file)
    const url = API_BASE + res.data.url
    document.execCommand('insertImage', false, url)
    onInput()
  } catch {
    ElMessage.error('图片上传失败')
  }
  ;(e.target as HTMLInputElement).value = ''
}
watch(
  () => props.modelValue,
  (v) => {
    if (editorRef.value && v !== editorRef.value.innerHTML) {
      editorRef.value.innerHTML = v || ''
    }
  }
)
</script>

<style scoped>
.rich-editor {
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;
}
.toolbar {
  display: flex;
  gap: 4px;
  padding: 8px;
  background: #f5f7f8;
  border-bottom: 1px solid var(--border);
}
.toolbar button {
  width: 32px;
  height: 32px;
  border: 1px solid var(--border);
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
}
.toolbar button:hover {
  border-color: var(--primary);
  color: var(--primary);
}
.editor {
  min-height: 320px;
  padding: 16px;
  outline: none;
  line-height: 1.8;
}
.editor:empty::before {
  content: '请输入图文内容…';
  color: var(--text-3);
}
.editor img {
  max-width: 100%;
  border-radius: 6px;
  margin: 8px 0;
}
</style>
