const { createApp } = Vue;

createApp({
    data() {
        return {
            // URL do backend (ajustar depois)
            apiUrl: 'http://localhost:5000/api',
            
            // Dados
            turmas: [],
            alunos: [],
            turmaSelecionada: '',
            dataAtual: new Date().toISOString().split('T')[0],
            
            // Toast
            toast: {
                show: false,
                message: '',
                type: 'success'
            }
        }
    },

    computed: {
        totalAlunos() {
            return this.alunos.length;
        },

        totalPresentes() {
            return this.alunos.filter(a => a.presente).length;
        },

        totalAusentes() {
            return this.alunos.filter(a => !a.presente).length;
        }
    },

    methods: {
        async carregarTurmas() {
            try {
                // Temporário: dados mockados
                // Depois substituir por: const res = await axios.get(`${this.apiUrl}/turmas`);
                this.turmas = [
                    { id: 1, nome: '1º Ano A - Matemática' },
                    { id: 2, nome: '1º Ano B - Matemática' },
                    { id: 3, nome: '2º Ano A - Física' }
                ];
            } catch (error) {
                this.mostrarToast('Erro ao carregar turmas', 'error');
                console.error(error);
            }
        },

        async carregarAlunos() {
            if (!this.turmaSelecionada) {
                this.alunos = [];
                return;
            }

            try {
                // Temporário: dados mockados
                // Depois substituir por: 
                // const res = await axios.get(`${this.apiUrl}/turmas/${this.turmaSelecionada}/alunos`);
                
                this.alunos = [
                    { id: 1, nome: 'Ana Silva', matricula: '2024001', presente: true },
                    { id: 2, nome: 'Bruno Costa', matricula: '2024002', presente: true },
                    { id: 3, nome: 'Carlos Santos', matricula: '2024003', presente: false },
                    { id: 4, nome: 'Diana Oliveira', matricula: '2024004', presente: true },
                    { id: 5, nome: 'Eduardo Lima', matricula: '2024005', presente: true },
                    { id: 6, nome: 'Fernanda Souza', matricula: '2024006', presente: false },
                    { id: 7, nome: 'Gabriel Pereira', matricula: '2024007', presente: true },
                    { id: 8, nome: 'Helena Rodrigues', matricula: '2024008', presente: true }
                ];
            } catch (error) {
                this.mostrarToast('Erro ao carregar alunos', 'error');
                console.error(error);
            }
        },

        marcarPresenca(aluno, presente) {
            aluno.presente = presente;
        },

        async salvarPresencas() {
            try {
                const dados = {
                    turma_id: this.turmaSelecionada,
                    data: this.dataAtual,
                    presencas: this.alunos.map(a => ({
                        aluno_id: a.id,
                        presente: a.presente
                    }))
                };

                // Temporário: apenas log
                console.log('Salvando presenças:', dados);
                
                // Depois descomentar:
                // await axios.post(`${this.apiUrl}/presencas`, dados);
                
                this.mostrarToast('✓ Presenças salvas com sucesso!', 'success');
            } catch (error) {
                this.mostrarToast('✗ Erro ao salvar presenças', 'error');
                console.error(error);
            }
        },

        mostrarToast(message, type = 'success') {
            this.toast.message = message;
            this.toast.type = type;
            this.toast.show = true;

            setTimeout(() => {
                this.toast.show = false;
            }, 3000);
        }
    },

    mounted() {
        this.carregarTurmas();
    }
}).mount('#app');
